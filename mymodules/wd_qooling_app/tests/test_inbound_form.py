import base64

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestQoolingInboundForm(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_group = cls.env.ref("wd_qooling_app.group_qooling_inbound_user")
        cls.internal_group = cls.env.ref("base.group_user")
        cls.user = cls.env["res.users"].create({
            "name": "Inbound Operator",
            "login": "inbound.operator",
            "email": "inbound.operator@example.com",
            "groups_id": [(6, 0, [cls.user_group.id, cls.internal_group.id])],
        })
        cls.warehouse = cls.env["stock.warehouse"].search([], limit=1)

    def _draft_values(self):
        return {
            "location_id": self.warehouse.id,
            "supervisor_id": self.user.id,
            "goods_status": "free_union_goods",
            "unloading_permission": "yes",
            "adr": "no",
        }

    def test_create_and_save_draft(self):
        record = self.env["wd.qooling.inbound.form"].with_user(self.user).create(self._draft_values())
        self.assertTrue(record.name.startswith("INB/"))
        self.assertEqual(record.state, "draft")
        self.assertEqual(record.filled_in_by_id, self.user)
        record.write({"comments": "Recorded without automatic action."})
        self.assertEqual(record.comments, "Recorded without automatic action.")

    def test_submit_requires_signature(self):
        record = self.env["wd.qooling.inbound.form"].with_user(self.user).create(self._draft_values())
        with self.assertRaises(UserError):
            record.action_submit()

    def test_submit_persists_submission_and_signature(self):
        record = self.env["wd.qooling.inbound.form"].with_user(self.user).create(self._draft_values())
        record.write({"warehouse_signature": "c2lnbmF0dXJl"})
        record.action_submit()
        self.assertEqual(record.state, "submitted")
        self.assertEqual(record.submitted_by_id, self.user)
        self.assertTrue(record.submitted_at)
        self.assertEqual(record.signer_id, self.user)
        self.assertTrue(record.signature_time)

    def test_adr_requires_related_fields_on_submit(self):
        record = self.env["wd.qooling.inbound.form"].with_user(self.user).create({
            **self._draft_values(),
            "adr": "yes",
            "warehouse_signature": "c2lnbmF0dXJl",
        })
        with self.assertRaises(UserError):
            record.action_submit()
        record.write({
            "un_number": "3171",
            "temperature_measured": "yes",
            "pallet_temperature_registered": "yes",
        })
        record.action_submit()
        self.assertEqual(record.state, "submitted")

    def test_record_values_do_not_create_workflow(self):
        record = self.env["wd.qooling.inbound.form"].with_user(self.user).create({
            **self._draft_values(),
            "packaging_condition": "not_good",
            "unloading_permission": "no_stop_unloading",
            "gas_measurement_status": "dangerous",
            "warehouse_signature": "c2lnbmF0dXJl",
        })
        record.action_submit()
        self.assertEqual(record.state, "submitted")
        self.assertEqual(record.packaging_condition, "not_good")
        self.assertEqual(record.unloading_permission, "no_stop_unloading")
        self.assertEqual(record.gas_measurement_status, "dangerous")

    def test_reset_to_draft(self):
        record = self.env["wd.qooling.inbound.form"].with_user(self.user).create({
            **self._draft_values(),
            "warehouse_signature": "c2lnbmF0dXJl",
        })
        record.action_submit()
        record.action_reset_to_draft()
        self.assertEqual(record.state, "draft")
        self.assertTrue(record.warehouse_signature)

    def test_optional_photos_and_comments(self):
        record = self.env["wd.qooling.inbound.form"].with_user(self.user).create({
            **self._draft_values(),
            "warehouse_signature": "c2lnbmF0dXJl",
        })
        record.action_submit()
        self.assertFalse(record.photo_ids)
        self.assertFalse(record.comments)
        self.assertTrue(fields.Datetime.to_datetime(record.submitted_at))

    def test_multiple_photos_are_related_attachments(self):
        record = self.env["wd.qooling.inbound.form"].with_user(self.user).create(self._draft_values())
        attachments = self.env["ir.attachment"].with_user(self.user).create([
            {
                "name": "damage-1.jpg",
                "datas": base64.b64encode(b"photo-1"),
                "mimetype": "image/jpeg",
                "res_model": record._name,
                "res_id": record.id,
            },
            {
                "name": "damage-2.jpg",
                "datas": base64.b64encode(b"photo-2"),
                "mimetype": "image/jpeg",
                "res_model": record._name,
                "res_id": record.id,
            },
        ])
        record.write({"photo_ids": [(6, 0, attachments.ids)]})
        self.assertEqual(record.photo_ids, attachments)
        record.write({"photo_ids": [(3, attachments[0].id)]})
        self.assertEqual(record.photo_ids, attachments[1])
