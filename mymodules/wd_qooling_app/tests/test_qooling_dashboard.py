from odoo.tests.common import TransactionCase


class TestQoolingDashboard(TransactionCase):
    def test_dashboard_and_forms_menu_structure(self):
        dashboard_action = self.env.ref("wd_qooling_app.action_qooling_dashboard")
        root_menu = self.env.ref("wd_qooling_app.menu_qooling_root")
        forms_menu = self.env.ref("wd_qooling_app.menu_qooling_forms")
        web_menu = self.env.ref("wd_qooling_app.menu_qooling_forms_web")
        pda_menu = self.env.ref("wd_qooling_app.menu_qooling_forms_pda")

        self.assertEqual(dashboard_action.tag, "qooling_dashboard")
        self.assertEqual(root_menu.action, dashboard_action)
        self.assertEqual(forms_menu.parent_id, root_menu)
        self.assertEqual(web_menu.parent_id, forms_menu)
        self.assertEqual(pda_menu.parent_id, forms_menu)
        self.assertEqual(pda_menu.name, "PDA")
        pda_action = self.env.ref("wd_qooling_app.action_qooling_inbound_pda")
        pda_inbound_menu = self.env.ref("wd_qooling_app.menu_qooling_inbound_pda")
        self.assertEqual(pda_inbound_menu.parent_id, pda_menu)
        self.assertEqual(pda_inbound_menu.action, pda_action)
        self.assertEqual(pda_action.tag, "wd_qooling_inbound_pda_dashboard")
        pda_form_action = self.env.ref("wd_qooling_app.action_qooling_inbound_pda_form")
        self.assertEqual(pda_form_action.tag, "wd_qooling_inbound_pda")
        self.assertEqual(
            self.env.ref("wd_qooling_app.action_qooling_outbound_pda").tag,
            "wd_qooling_outbound_pda_dashboard",
        )
        self.assertEqual(
            self.env.ref("wd_qooling_app.action_qooling_outbound_pda_form").tag,
            "wd_qooling_outbound_pda",
        )
        self.assertEqual(
            self.env.ref("wd_qooling_app.action_qooling_temperature_pda").tag,
            "wd_qooling_temperature_pda_dashboard",
        )
        self.assertEqual(
            self.env.ref("wd_qooling_app.action_qooling_temperature_pda_form").tag,
            "wd_qooling_temperature_pda",
        )

        for xml_id in (
            "menu_qooling_inbound",
            "menu_qooling_outbound",
            "menu_qooling_temperature_record",
        ):
            menu = self.env.ref("wd_qooling_app.%s" % xml_id)
            self.assertEqual(menu.parent_id, web_menu)
