/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class PdaRecordDashboard extends Component {
    static template = "wd_qooling_app.PdaRecordDashboard";
    static props = { "*": true };
    static config = {};

    setup() {
        this.openRecord = this.openRecord.bind(this);
        this.createRecord = this.createRecord.bind(this);
        this.backToDashboard = this.backToDashboard.bind(this);
        this.action = useService("action");
        this.orm = useService("orm");
        this.state = useState({ records: [], loading: true, error: "" });
        onWillStart(() => this.loadRecords());
    }

    get dashboardConfig() {
        return this.constructor.config;
    }

    async loadRecords() {
        const config = this.constructor.config;
        this.state.loading = true;
        this.state.error = "";
        try {
            const records = await this.orm.searchRead(
                config.model,
                [],
                config.fields,
                { order: "id desc", limit: 100 },
            );
            this.state.records = records.map((record) => ({
                ...record,
                dateValue: record[config.dateField] || "",
                referenceValue: config.referenceFields
                    .map((field) => record[field])
                    .find((value) => value) || "",
            }));
        } catch (error) {
            this.state.error = error.data?.message || error.message || "Could not load PDA records.";
        } finally {
            this.state.loading = false;
        }
    }

    openRecord(record) {
        return this.action.doAction(this.constructor.config.formAction, {
            additionalContext: { active_id: record.id },
        });
    }

    createRecord() {
        return this.action.doAction(this.constructor.config.formAction, {
            additionalContext: { new_record: true },
        });
    }

    backToDashboard() {
        return this.action.doAction("wd_qooling_app.action_qooling_dashboard");
    }
}

class InboundPdaRecordDashboard extends PdaRecordDashboard {
    static config = {
        title: "Inbound Record",
        model: "wd.qooling.inbound.form",
        fields: ["name", "state", "date", "ref_no", "container_shipment_number"],
        dateField: "date",
        referenceFields: ["ref_no", "container_shipment_number"],
        formAction: "wd_qooling_app.action_qooling_inbound_pda_form",
    };
}

class OutboundPdaRecordDashboard extends PdaRecordDashboard {
    static config = {
        title: "Outbound Record",
        model: "wd.qooling.outbound.form",
        fields: ["name", "state", "date_arrival", "ref_no", "mrn_number"],
        dateField: "date_arrival",
        referenceFields: ["ref_no", "mrn_number"],
        formAction: "wd_qooling_app.action_qooling_outbound_pda_form",
    };
}

class TemperaturePdaRecordDashboard extends PdaRecordDashboard {
    static config = {
        title: "Temperature Record",
        model: "wd.qooling.temperature.record",
        fields: ["name", "state", "date", "customer", "container_number"],
        dateField: "date",
        referenceFields: ["customer", "container_number"],
        formAction: "wd_qooling_app.action_qooling_temperature_pda_form",
    };
}

registry.category("actions").add("wd_qooling_inbound_pda_dashboard", InboundPdaRecordDashboard);
registry.category("actions").add("wd_qooling_outbound_pda_dashboard", OutboundPdaRecordDashboard);
registry.category("actions").add("wd_qooling_temperature_pda_dashboard", TemperaturePdaRecordDashboard);
