const EP_HOST = "https://empathy-polls-be.herokuapp.com";
const API_HOST = "https://empathy-polls-be.herokuapp.com/polls";

const API_EVENT = API_HOST + "/vote_session";
const API_TIMESLOT = API_HOST + "/timeslot";
const API_VOTES = API_HOST + "/vote";

const PREFERENCES = {
    "UN": 4, "LE": 3, "OK": 2, "MOST": 1,
    4: "UN", 3: "LE", 2: "OK", 1: "MOST"
};

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


if (!window.httpGet || !window.httpPost) {
    throw new Error("Not initalized session");
}

async function getVoteDetail(vote_id) {
    let vote_detail = await window.httpGet(`${API_EVENT}/${vote_id}?format=json`);
    let result = {};
    if (typeof vote_detail.uuid == 'undefined') {
        return result;
    }
    result = {
        'event_name': vote_detail.title,
        'place': vote_detail.place,
        'is_mandatory': vote_detail.is_mandatory,
        'is_opened': vote_detail.open_public,
        'is_finished': vote_detail.is_finished,
        'notes': vote_detail.notes,
        'total_slots': 0,
        'slots': [],
        'voted': [],
        'votes': []
    };

    let [ts, s] = parseTimeslots(vote_detail.timeslots);
    let [vn, vr] = parseVotes(vote_detail.votes);

    result.total_slots = ts;
    result.slots = s;
    result.voted = vn;
    result.votes = vr;
    console.log(result);
    return result;
}

function parseTimeslots(timeslots) {
    let result = {};
    let slotids = {}

    for (let i = 0; i < timeslots.length; i++) {
        let d = new Date(timeslots[i].datetime);
        let date = `${MONTHS[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()} (${DAYS[d.getDay()]})`;
        let time = `${("0" + d.getHours()).slice(-2)}:${("0" + d.getMinutes()).slice(-2)}`;
        if (typeof result[date] == 'undefined') {
            result[date] = [];
            slotids[date] = [];
        }
        result[date].push(time);
        slotids[date].push(timeslots[i].id);
    }
    console.log(result);
    let real_result = [];
    let dates = Object.keys(result);
    for (let i = 0; i < dates.length; i++) {
        real_result.push({
            "date": dates[i],
            "times": result[dates[i]],
            "slotids": slotids[dates[i]]
        });
    }

    return [timeslots.length, real_result];
}

function parseVotes(votes) {
    let result = {};

    votes.sort((x, y) => {
        if (x.voter_name > y.voter_name) return 1;
        if (x.voter_name < y.voter_name) return -1;
        if (x.timeslot_id > y.timeslot_id) return 1;
        if (x.timeslot_id < y.timeslot_id) return -1;
        return 0;
    });

    for (let i = 0; i < votes.length; i++) {
        let name = votes[i].voter_name;
        if (typeof result[name] == 'undefined') {
            result[name] = [];
        }
        result[name].push({
            "priority": PREFERENCES[votes[i].preferences],
            "misc": votes[i].notes
        });
    }

    let voted_names = [];
    let voted_results = [];
    let names = Object.keys(result);
    for (let i = 0; i < names.length; i++) {
        voted_names.push(names[i]);
        voted_results.push(result[names[i]]);
    }

    return [voted_names, voted_results];
}

async function createVote(title, place, is_mandatory, open_public, notes) {
    return await window.httpPost(`${API_EVENT}/?format=json`, data = {
        title, place, is_mandatory, open_public, notes
    });
}

async function createTimeslot(uuid, datetime) {
    return await window.httpPost(`${API_TIMESLOT}/?format=json`, data = {
        datetime,
        "session_id": uuid
    });
}

async function saveTimeslot(vote_id, slot_id, name, priority, notes) {
    return await window.httpPost(`${API_VOTES}/?format_json`, data = {
        "voter_name": name,
        "preferences": PREFERENCES[priority],
        notes,
        "session_id": vote_id,
        "timeslot_id": slot_id
    });
}