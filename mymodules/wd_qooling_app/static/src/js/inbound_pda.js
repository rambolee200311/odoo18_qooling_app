/** @odoo-module **/

import { Component, onPatched, onWillStart, onWillUnmount, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const STEPS = [
    { key: "details", label: "Details" },
    { key: "checks", label: "Checks" },
    { key: "adr", label: "ADR & temperature" },
    { key: "evidence", label: "Evidence & sign" },
];

export class QoolingInboundPda extends Component {
    static template = "wd_qooling_app.InboundPda";
    static props = {};

    setup() {
        this.setValue = this.setValue.bind(this);
        this.deletePhoto = this.deletePhoto.bind(this);
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");
        this.signatureCanvas = useRef("signatureCanvas");
        this.state = useState({
            record: { date: new Date().toISOString().slice(0, 10), filing_date: new Date().toISOString().slice(0, 10), adr: "no" },
            warehouses: [],
            users: [],
            recordId: null,
            photos: [],
            step: 0,
            busy: false,
            error: "",
            saved: "",
            preview: false,
        });
        onWillStart(async () => {
            [this.state.warehouses, this.state.users] = await Promise.all([
                this.orm.searchRead("stock.warehouse", [], ["name"], { limit: 100 }),
                this.orm.searchRead("res.users", [["share", "=", false]], ["name"], { limit: 100 }),
            ]);
        });
        onPatched(() => {
            if (this.state.step === 3 && this.signatureCanvas.el !== this.signatureElement) {
                this.teardownSignature();
                this.setupSignature();
            }
        });
        onWillUnmount(() => this.teardownSignature());
    }

    get steps() {
        return STEPS;
    }

    setValue(name, value) {
        this.state.record[name] = value;
        this.state.error = "";
    }

    onFieldChange(event) {
        const field = event.target.dataset.field;
        let value = event.target.type === "checkbox" ? event.target.checked : event.target.value;
        if (["location_id", "supervisor_id"].includes(field)) {
            value = Number(value);
        } else if (field === "average_temperature_per_pallet") {
            value = Number(value);
        }
        this.setValue(field, value);
    }

    async save() {
        this.state.busy = true;
        this.state.error = "";
        try {
            if (this.state.recordId) {
                await this.orm.write("wd.qooling.inbound.form", [this.state.recordId], this.state.record);
            } else {
                const [recordId] = await this.orm.create("wd.qooling.inbound.form", [this.state.record]);
                this.state.recordId = recordId;
            }
            await this.loadPhotos();
            this.state.saved = "Draft saved";
            this.notification.add("Inbound draft saved.", { type: "success" });
        } catch (error) {
            this.state.error = error.data?.message || error.message || "Could not save the draft.";
        } finally {
            this.state.busy = false;
        }
    }

    async submit() {
        this.state.busy = true;
        this.state.error = "";
        try {
            if (!this.state.recordId) {
                const [recordId] = await this.orm.create("wd.qooling.inbound.form", [this.state.record]);
                this.state.recordId = recordId;
            } else {
                await this.orm.write("wd.qooling.inbound.form", [this.state.recordId], this.state.record);
            }
            await this.orm.call("wd.qooling.inbound.form", "action_submit", [[this.state.recordId]]);
            this.state.record.state = "submitted";
            this.state.saved = "Submitted";
            this.notification.add("Inbound record submitted.", { type: "success" });
        } catch (error) {
            this.state.error = error.data?.message || error.message || "Could not submit the record.";
        } finally {
            this.state.busy = false;
        }
    }

    previous() {
        this.state.step = Math.max(0, this.state.step - 1);
    }

    next() {
        this.state.step = Math.min(STEPS.length - 1, this.state.step + 1);
    }

    openWebForm() {
        return this.action.doAction("wd_qooling_app.action_qooling_inbound_form", {
            additionalContext: this.state.recordId ? { active_id: this.state.recordId } : {},
        });
    }

    onPhoto(event) {
        if (!this.state.recordId) {
            this.state.error = "Save the draft before uploading photos.";
            event.target.value = "";
            return;
        }
        for (const file of event.target.files) {
            const reader = new FileReader();
            reader.onload = async () => {
                try {
                    const [attachmentId] = await this.orm.create("ir.attachment", [{
                        name: file.name,
                        datas: reader.result.split(",")[1],
                        mimetype: file.type,
                        res_model: "wd.qooling.inbound.form",
                        res_id: this.state.recordId,
                    }]);
                    await this.orm.write("wd.qooling.inbound.form", [this.state.recordId], {
                        photo_ids: [[4, attachmentId]],
                    });
                    await this.loadPhotos();
                } catch (error) {
                    this.state.error = error.data?.message || error.message || "Could not upload the photo.";
                }
            };
            reader.readAsDataURL(file);
        }
        event.target.value = "";
    }

    async loadPhotos() {
        if (!this.state.recordId) {
            this.state.photos = [];
            return;
        }
        const records = await this.orm.searchRead(
            "ir.attachment",
            [
                ["res_model", "=", "wd.qooling.inbound.form"],
                ["res_id", "=", this.state.recordId],
                ["res_field", "=", false],
            ],
            ["name", "mimetype"],
        );
        this.state.photos = records;
    }

    async deletePhoto(photoId) {
        if (!this.state.recordId) {
            return;
        }
        try {
            await this.orm.write("wd.qooling.inbound.form", [this.state.recordId], {
                photo_ids: [[3, photoId]],
            });
            await this.orm.unlink("ir.attachment", [photoId]);
            await this.loadPhotos();
        } catch (error) {
            this.state.error = error.data?.message || error.message || "Could not delete the photo.";
        }
    }

    setupSignature() {
        const canvas = this.signatureCanvas.el;
        if (!canvas) {
            return;
        }
        this.signatureElement = canvas;
        canvas.width = canvas.clientWidth || 500;
        canvas.height = 160;
        this.signatureContext = canvas.getContext("2d");
        this.signatureContext.lineWidth = 2;
        this.signatureContext.lineCap = "round";
        this.drawing = false;
        this.signatureStart = (event) => {
            this.drawing = true;
            canvas.setPointerCapture?.(event.pointerId);
            const rect = canvas.getBoundingClientRect();
            this.signatureContext.beginPath();
            this.signatureContext.moveTo(event.clientX - rect.left, event.clientY - rect.top);
        };
        this.signatureMove = (event) => {
            if (!this.drawing) return;
            const rect = canvas.getBoundingClientRect();
            this.signatureContext.lineTo(event.clientX - rect.left, event.clientY - rect.top);
            this.signatureContext.stroke();
            this.signatureContext.beginPath();
            this.signatureContext.moveTo(event.clientX - rect.left, event.clientY - rect.top);
        };
        this.signatureEnd = () => {
            if (!this.drawing) return;
            this.drawing = false;
            this.setValue("warehouse_signature", canvas.toDataURL("image/png").split(",")[1]);
        };
        canvas.addEventListener("pointerdown", this.signatureStart);
        canvas.addEventListener("pointermove", this.signatureMove);
        canvas.addEventListener("pointerup", this.signatureEnd);
        canvas.addEventListener("pointercancel", this.signatureEnd);
    }

    clearSignature() {
        this.signatureContext.clearRect(0, 0, this.signatureCanvas.el.width, this.signatureCanvas.el.height);
        this.setValue("warehouse_signature", false);
    }

    teardownSignature() {
        const canvas = this.signatureElement;
        if (!canvas || !this.signatureStart) return;
        canvas.removeEventListener("pointerdown", this.signatureStart);
        canvas.removeEventListener("pointermove", this.signatureMove);
        canvas.removeEventListener("pointerup", this.signatureEnd);
        canvas.removeEventListener("pointercancel", this.signatureEnd);
        this.signatureElement = null;
        this.signatureContext = null;
    }
}

registry.category("actions").add("wd_qooling_inbound_pda", QoolingInboundPda);
