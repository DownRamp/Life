const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const SportsSchema = new Schema({
    userId: { type: String},
    name: { type: String },
    sport: { type: String },
    accuracy: { type: Schema.Types.Decimal128 },
    saves: { type: Schema.Types.Decimal128 },
    average: {type: Schema.Types.Decimal128},
    assists: { type: Schema.Types.Decimal128 },
    totalScore: { type: Number },
    fouls: {type: Schema.Types.Decimal128},
    steals: {type: Schema.Types.Decimal128},
    games: [
        {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Game",
            default: []
        }
    ],
    position: { type: String },
    division: { type: String }
});

const Sports = mongoose.model('Sports', SportsSchema);
module.exports = Sports;