const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(express.urlencoded({ extended: false }));

// Load the provided JSON data files[cite: 7]
const reviews_data = JSON.parse(fs.readFileSync("data/reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("data/dealerships.json", 'utf8'));

// Load models
const Dealership = require('./dealership');
const Review = require('./review');

// Connect to MongoDB
mongoose.connect('mongodb://mongo_db:27017/dealershipsDB');

// Populate the database with initial data on startup
Review.deleteMany({}).then(() => {
  Review.insertMany(reviews_data['reviews']);
});
Dealership.deleteMany({}).then(() => {
  Dealership.insertMany(dealerships_data['dealerships']);
});

// 1. Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Review.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// 2. Fetch reviews by dealer ID (Task 8)
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    // Parse the string ID from the URL to an integer to match the database schema
    const documents = await Review.find({ dealership: parseInt(req.params.id) });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews for dealer' });
  }
});

// 3. Fetch all dealerships (Task 9)
app.get('/fetchDealers', async (req, res) => {
  try {
    const dealerships = await Dealership.find();
    res.json(dealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// 4. Fetch dealerships by state (Task 11)
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const dealerships = await Dealership.find({ state: req.params.state });
    res.json(dealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// 5. Fetch dealer by ID (Task 10)
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    // Parse the string ID from the URL to an integer to match the database schema
    const dealership = await Dealership.findOne({ id: parseInt(req.params.id) });
    res.json(dealership);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealership by ID' });
  }
});

// 6. Insert review
app.post('/insert_review', express.json(), async (req, res) => {
  try {
    const data = req.body;
    const documents = await Review.create(data);
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error inserting review' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});