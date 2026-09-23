import base64

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestQoolingTemperatureRecord(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_group = cls.env.ref("wd_qooling_app.group_temperature_user")
        cls.supervisor_group = cls.env.ref("wd_qooling_app.group_temperature_supervisor")
        cls.internal_group = cls.env.ref("base.group_user")
        cls.operator = cls.env["res.users"].create({
            "name": "Temperature Operator",
            "login": "temperature.operator",
            "groups_id": [(6, 0, [cls.user_group.id, cls.internal_group.id])],
        })
        cls.supervisor = cls.env["res.users"].create({
            "name": "Temperature Supervisor",
            "login": "temperature.supervisor",
            "groups_id": [(6, 0, [cls.supervisor_group.id, cls.internal_group.id])],
        })
    def _values(self):
        return {
            "customer": "Temperature Customer",
            "container_number": "CONT-TMP-1",
            "manager_id": self.supervisor.id,
        }

    def test_create_sequence_and_dynamic_pallets(self):
        record = self.env["wd.qooling.temperature.record"].with_user(self.operator).create(self._values())
        self.assertTrue(record.name.startswith("TMP/"))
        lines = self.env["wd.qooling.temperature.record.line"].with_user(self.operator).create([
            {"record_id": record.id, "temperature": -18},
            {"record_id": record.id, "temperature": -17.5},
        ])
        self.assertEqual(lines.mapped("pallet_number"), ["pallet1", "pallet2"])
        self.assertEqual(record.total_pallets, 2)
        lines[0].temperature = -16
        self.assertEqual(lines[0].temperature, -16)

    def test_line_delete_is_forbidden_but_clear_action_restarts_numbering(self):
        record = self.env["wd.qooling.temperature.record"].with_user(self.operator).create(self._values())
        line = self.env["wd.qooling.temperature.record.line"].with_user(self.operator).create(
            {"record_id": record.id}
        )
        with self.assertRaises(UserError):
            line.unlink()
        record.action_clear_lines()
        new_line = self.env["wd.qooling.temperature.record.line"].with_user(self.operator).create(
            {"record_id": record.id}
        )
        self.assertEqual(new_line.pallet_number, "pallet1")

    def test_submit_requires_signature_and_supervisor_actions(self):
        record = self.env["wd.qooling.temperature.record"].with_user(self.operator).create(self._values())
        with self.assertRaises(UserError):
            record.action_submit()
        record.action_sign(base64.b64encode(b"signature"))
        record.action_submit()
        self.assertEqual(record.state, "submitted")
        record.with_user(self.supervisor).action_mark_exception()
        record.with_user(self.supervisor).action_close()
        self.assertEqual(record.state, "closed")

    def test_multiple_evidence_photos_are_supported(self):
        record = self.env["wd.qooling.temperature.record"].with_user(self.operator).create(self._values())
        attachment = self.env["ir.attachment"].create({
            "name": "temperature.jpg",
            "datas": "dGVzdA==",
            "res_model": record._name,
            "res_id": record.id,
        })
        record.write({"photo_ids": [(4, attachment.id)]})
        self.assertIn(attachment, record.photo_ids)
