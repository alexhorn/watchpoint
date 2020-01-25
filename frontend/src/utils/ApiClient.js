import {api_base} from './config.js';

export default class ApiClient {

    constructor() {
        this.base = api_base;
    }

    async getDevices() {
        const resp = await fetch(`${this.base}/devices`);
        return await resp.json();
    }

    async getDevice(device_id) {
        if (!Number.isInteger(device_id))
            throw new Error("Invalid device_id");

        const resp = await fetch(`${this.base}/devices/${device_id}`);
        return await resp.json();
    }

    async updateDevice(device_id, data) {
        const resp = await fetch(`${this.base}/devices/${device_id}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        return await resp.json();
    }

}
