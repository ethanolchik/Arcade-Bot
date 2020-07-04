const TicTacToe = require('discord-tictactoe');
/**
 * what? you seriously thought i was gonna write the tic-tac-toe myself in JS?
 * nah. i ain't ever gonna do that. i hate JS, thats why.
 */
const fs = require('fs');
fs.readFile('./db/js-creds.json', 'utf8', (err, jsonString) => {
    if (err) {
        return
    }
    try {
        const creds = JSON.parse(jsonString)
        const bot = new TicTacToe({
            clientId: creds.clientid,
            token: creds.token,
            language: 'en',
            command: 'arc!ttt'
        });
        console.log("connecting")
        bot.connect()
        console.log("connected")
} catch(err) {
    }
})
