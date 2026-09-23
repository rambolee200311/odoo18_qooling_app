from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError, UserError
from odoo.tests.common import TransactionCase


class TestQoolingOutboundForm(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.operator_group = cls.env.ref("wd_qooling_app.group_qooling_outbound_user")
        cls.reviewer_group = cls.env.ref("wd_qooling_app.group_qooling_outbound_reviewer")
        cls.internal_group = cls.env.ref("base.group_user")
        cls.operator = cls.env["res.users"].create({
            "name": "Outbound Operator",
            "login": "outbound.operator",
            "groups_id": [(6, 0, [cls.operator_group.id, cls.internal_group.id])],
        })
        cls.reviewer = cls.env["res.users"].create({
            "name": "Outbound Reviewer",
            "login": "outbound.reviewer",
            "groups_id": [(6, 0, [cls.reviewer_group.id, cls.internal_group.id])],
        })
        cls.warehouse = cls.env["stock.warehouse"].search([], limit=1)

    def _values(self):
        arrival = fields.Datetime.now()
        return {
            "location_id": self.warehouse.id,
            "date_arrival": arrival,
            "start_loading_at": arrival + timedelta(minutes=5),
            "end_loading_at": arrival + timedelta(minutes=10),
            "supervisor_id": self.reviewer.id,
            "goods_type": "bonded",
            "adr": "no",
            "ref_no": "OUT-TEST-1",
        }

    def _signed_record(self):
        record = self.env["wd.qooling.outbound.form"].with_user(self.operator).create(self._values())
        record.action_sign_driver("driver-image")
        record.action_sign_warehouse("warehouse-image")
        return record

    def test_create_save_and_reread_draft(self):
        record = self.env["wd.qooling.outbound.form"].with_user(self.operator).create(self._values())
        self.assertTrue(record.name.startswith("OUT/"))
        record.write({"driver_comments": "Keep original inspection result."})
        reread = self.env["wd.qooling.outbound.form"].browse(record.id)
        self.assertEqual(reread.driver_comments, "Keep original inspection result.")
        self.assertEqual(reread.state, "draft")

    def test_submit_allows_optional_signatures(self):
        record = self.env["wd.qooling.outbound.form"].with_user(self.operator).create(self._values())
        record.action_submit()
        self.assertEqual(record.state, "submitted")
        record = self.env["wd.qooling.outbound.form"].with_user(self.operator).create(self._values())
        record.action_sign_driver("driver-image")
        record.action_submit()
        self.assertEqual(record.state, "submitted")
        self.assertEqual(record.driver_signer_id, self.operator)
        self.assertFalse(record.warehouse_signer_id)
        self.assertTrue(record.submitted_at)
        record = self.env["wd.qooling.outbound.form"].with_user(self.operator).create(self._values())
        record.action_sign_warehouse("warehouse-image")
        record.action_submit()
        self.assertEqual(record.warehouse_signer_id, self.operator)

    def test_loading_times_must_be_ordered(self):
        values = self._values()
        values["end_loading_at"] = values["date_arrival"] - timedelta(minutes=1)
        with self.assertRaises(UserError):
            self.env["wd.qooling.outbound.form"].with_user(self.operator).create(values)

    def test_un_number_and_evidence_are_recorded_without_automation(self):
        record = self._signed_record()
        record.write({
            "adr": "yes",
            "un_number": "3480",
            "measured_temperature": -18,
            "weight_distribution": False,
            "cargo_photo": "photo",
            "driver_comments": "Temperature recorded for review.",
        })
        record.action_submit()
        self.assertEqual(record.state, "submitted")
        self.assertEqual(record.un_number, "3480")
        self.assertFalse(record.weight_distribution)
        self.assertEqual(record.cargo_photo, "photo")
        attachment = self.env["ir.attachment"].create({
            "name": "outbound-photo.jpg", "datas": "photo",
            "res_model": "wd.qooling.outbound.form", "res_id": record.id,
        })
        record.write({"photo_ids": [(4, attachment.id)]})
        self.assertEqual(record.photo_ids, attachment)

    def test_reviewer_can_mark_and_reset_manual_state(self):
        record = self._signed_record()
        record.with_user(self.operator).action_submit()
        record.with_user(self.reviewer).action_mark_exception()
        self.assertEqual(record.state, "exception_pending")
        record.with_user(self.reviewer).action_reset_to_draft()
        self.assertEqual(record.state, "draft")

    def test_unauthorized_user_has_no_access(self):
        user = self.env["res.users"].create({
            "name": "No Outbound Access",
            "login": "no.outbound.access",
            "groups_id": [(6, 0, [self.internal_group.id])],
        })
        with self.assertRaises(AccessError):
            self.env["wd.qooling.outbound.form"].with_user(user).search([])
