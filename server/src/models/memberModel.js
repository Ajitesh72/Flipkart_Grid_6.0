const mongoose = require('mongoose');

const memberSchema = new mongoose.Schema(
    {
        registerId: {
            type: String,
            unique: true,
            required: true,
        },
        firstName: {
            type: String,
            required: true,
        },
        lastName: {
            type: String,
            required: true,
        },
        email: {
            type: String,
            required: true,
            unique: true,
        },
        contactNo: {
            type: String,
            required: true,
        },
        age: {
            type: Number,
            required: true,
        },
        address1: {
            type: String,
            required: true,
        },
        role: {
            type: String,
            required: true,
        },
    },
    { timestamps: true }
);

module.exports = mongoose.model('Member', memberSchema);
