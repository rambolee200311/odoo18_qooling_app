/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { FileInput } from "@web/core/file_input/file_input";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useX2ManyCrud } from "@web/views/fields/relational_utils";

export class QoolingPhotoGalleryField extends Component {
    static template = "wd_qooling_app.QoolingPhotoGalleryField";
    static components = { FileInput };
    static props = { ...standardFieldProps };

    setup() {
        this.onFileRemove = this.onFileRemove.bind(this);
        this.openPreview = this.openPreview.bind(this);
        this.notification = useService("notification");
        this.operations = useX2ManyCrud(() => this.props.record.data[this.props.name], true);
        this.state = useState({ previewId: null });
    }

    get files() {
        return this.props.record.data[this.props.name].records.map((record) => ({
            id: record.resId,
            name: record.data.name,
            mimetype: record.data.mimetype,
        }));
    }

    getUrl(id) {
        return `/web/content/${id}`;
    }

    async onFileUploaded(files) {
        for (const file of files) {
            if (file.error) {
                this.notification.add(file.error, { type: "danger" });
                continue;
            }
            await this.operations.saveRecord([file.id]);
        }
    }

    async onFileRemove(id) {
        const record = this.props.record.data[this.props.name].records.find(
            (candidate) => candidate.resId === id
        );
        if (record) {
            await this.operations.removeRecord(record);
        }
    }

    openPreview(id) {
        this.state.previewId = id;
    }

    closePreview() {
        this.state.previewId = null;
    }
}

registry.category("fields").add("qooling_photo_gallery", {
    component: QoolingPhotoGalleryField,
    supportedTypes: ["many2many"],
});
