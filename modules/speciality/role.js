// Taken from the Custom Role system in CAutomator.py and enhanced a bit.
// Thanks to http://github.com/iwa for the original code!

// Importing prefix
const config = require('../../data/config.json');
let prefix = config.PREFIX

// Set up database based on lowdb.
const lowdb = require("lowdb");
const FileSync = require('lowdb/adapters/FileSync')
const adapter = new FileSync(`${config.DIR}/data/database.json`)
const db = lowdb(adapter)
db.defaults({ roles: [], rcount: 0, profiles: [], pcount: 0 })
        .write()

module.exports = {
    commands: 'role',
    minArgs: 0,
    maxArgs: 500,
    requiredRoles: ['Level 30+'],
    callback: (message, args) => {
        let rolename = "";
        let search = db.get('roles')
            .find({memberid: message.author.id})
            .value()
        message.react('<a:typing:798907891787628544>')
        if (!search) {
            for (let x = 1; x < (args.length); x++) {
                rolename = `${rolename} ${args[x]}`
            }
            if (/^(?:[0-9a-fA-F]{3}){1,2}$/.test(args[0])) {
                let rolecolour = parseInt(args[0], 16)
                let pos = db.get('rcount').value()
                message.guild.roles.create({
                    data: {
                      name: rolename,
                      color: rolecolour,
                      hoist: true,
                      position: message.guild.roles.cache.size-pos
                    },
                  })
                    .then(role => {
                        db.get('roles')
                            .push({memberid: message.author.id, roleid: role.id})
                            .write()
                        message.member.roles.add(role.id)
                        db.update('rcount', n => n + 1)
                            .write()
                        message.reply(`I've created your custom role: <@&${role.id}>`)
                    })
                    .catch(console.error);
            } else {
                message.reply('you didn\'t specify a colour (or didn\'t specify it properly)! Do in the following format: `~role <colour> <role name>`')
            }
        } else {
            if (args[0] == "remove") {
                message.member.roles.remove(search.roleid)
                    .then(message.reply('I\'ve removed your custom role.'))
                return
            }
            for (let x = 1; x < (args.length); x++) {
                rolename = `${rolename} ${args[x]}`
            }
            if (/^(?:[0-9a-fA-F]{3}){1,2}$/.test(args[0])) {
                let rolecolour = parseInt(args[0], 16)
                message.guild.roles.fetch(search.roleid)
                    .then(role => {
                        role.edit({
                            name: rolename,
                            color: rolecolour
                        })
                        message.reply(`I've edited your custom role: <@&${role.id}>`)
                        try {
                            message.member.roles.add(role.id)
                        } catch { console.log('Member may already have role') }
                    })
            } else {
                message.reply('you didn\'t specify a colour (or didn\'t specify it properly)! Do in the following format: `~role <colour> <role name>`')
            }
        }
        message.reactions.removeAll()
    }
}