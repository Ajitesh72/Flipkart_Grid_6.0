const Member = require('../models/memberModel');
const { v4: uuidv4 } = require('uuid');

// Get all members
const getAllMembers = async (req, res) => {
    try {
        const members = await Member.find();
        res.status(200).json(members);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

// Get a specific member
const getMemberById = async (req, res) => {
    try {
        const member = await Member.findOne({ registerId: req.params.id });
        if (!member) return res.status(404).json({ message: 'Member not found' });
        res.status(200).json(member);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

// Add a new member
const addMember = async (req, res) => {
    try {
        const { firstName, lastName, email, contactNo, age, address1, role } = req.body;

        // Generate a new member object with a unique register ID
        const newMember = {
            registerId: uuidv4(),
            firstName,
            lastName,
            email,
            contactNo,
            age,
            address1,
            role,
        };

        
        res.status(200).json(newMember);
    }catch(error){
        res.status(400).json({ message: error.message });
    }




    // try {
    //     const { firstName, lastName, email, contactNo, age, address1, role } = req.body;

    //     const newMember = new Member({
    //         registerId: uuidv4(),
    //         firstName,
    //         lastName,
    //         email,
    //         contactNo,
    //         age,
    //         address1,
    //         role,
    //     });

    //     const savedMember = await newMember.save();
    //     res.status(201).json(savedMember);
    // } catch (error) {
    //     res.status(400).json({ message: error.message });
    // }
};

// Update a member
const updateMember = async (req, res) => {
    try {
        const updatedMember = await Member.findOneAndUpdate(
            { registerId: req.params.id },
            req.body,
            { new: true }
        );
        if (!updatedMember) return res.status(404).json({ message: 'Member not found' });
        res.status(200).json(updatedMember);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

// Delete a member
const deleteMember = async (req, res) => {
    try {
        const deletedMember = await Member.findOneAndDelete({ registerId: req.params.id });
        if (!deletedMember) return res.status(404).json({ message: 'Member not found' });
        res.status(200).json({ message: 'Member deleted successfully' });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

module.exports = {
    getAllMembers,
    getMemberById,
    addMember,
    updateMember,
    deleteMember,
};
