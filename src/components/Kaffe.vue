<template>
  <div v-if="interaction" class="kaffe-wrapper">
    <div class="kaffe-score" v-if="scoring">
      <div v-if="!card">
        <img src="@/assets/scan.gif" alt="scan" class="scan" />
        <h3>Select cups amount on keypad</h3>
        <h1>{{ amount }} cups</h1>
        <h2>Scan card after the correct amount is selected</h2>
      </div>

      <div v-if="card && userExists && paid">
        <h1>{{ amount }} cups registered!</h1>
        <font-awesome-icon :icon="['fas', 'mug-hot']" size="6x" />
        <h2>Your score is {{ scoreCount }}</h2>
      </div>

      <div v-if="card && !userExists">
        <h1>You must register before you can score!</h1>
        <h2>Please pay first and start scoring!</h2>
      </div>

      <div v-if="card && userExists && !paid">
        <h1>Looks like it's been >180 days since you paid last time!</h1>
        <h2>Please pay first and start scoring!</h2>
      </div>
    </div>

    <div v-if="help" class="help">
      <h1>Help!</h1>
      <div>
        <h3>Register</h3>
        <hr>
        <p>Press Pay, scan your student card, scan the QR code, press pay again and you're registered for the next 180 days!</p>
      </div>
      <div>
        <h3>Score coffee</h3>
        <hr>
        <p>Press Score Coffee, select the amount of cups you want to register with the knob, then scan your student card.</p>
      </div>
      <div>
        <h3>Show score</h3>
        <hr>
        <p>Press Show Score, scan your student card.</p>
      </div>
      <div>
        <h3>Useful</h3>
        <hr>
        <p>You can cancel with the orange button</p>
      </div>
    </div>

    <div class="kaffe-score" v-if="register">

      <div v-if="card && !alreadyPaid && !paid">
        <h1>Register!</h1>
        <img src="@/assets/qr.png" alt="scan" id="qr" />
        <h2>Please pay, then press the Pay button to continue!</h2>
        <h3>Press the orange button if you wish to cancel!</h3>
      </div>

      <div v-if="card && paid && !alreadyPaid">
        <h1>You are now registered!</h1>
        <h2>You will have to pay again in 180 days to continue scoring coffee.</h2>
      </div>

      <div v-if="card && alreadyPaid">
        <h1>You have already paid for this half year!</h1>
      </div>

      <div v-if="!card">
        <img src="@/assets/scan.gif" alt="scan" class="scan" />
        <h2>Scan card to register</h2>
      </div>

    </div>

    <div class="kaffe-show-score" v-if="showScore">
      <div v-if="!card">
        <img src="@/assets/scan.gif" alt="scan" class="scan" />
        <h2>Scan card to show your score</h2>
      </div>

      <div v-if="(card && userExists)">
        <h2>Your score is {{ scoreCount }}</h2>
        <font-awesome-icon :icon="['fas', 'mug-hot']" size="6x" />
      </div>

      <div v-if="card && !userExists">
        <h1>You don't have any score!</h1>
        <h2>Please pay first and start scoring!</h2>
      </div>
    </div>
  </div>
</template>

<script>
  let tm;
export default {
  name: "Kaffe",
  created: function () {
    window.addEventListener("keyup", this.onkey);
  },
  beforeDestroy: function () {
    window.removeEventListener("keyup", this.onkey);
  },
  data() {
    return {
      card: false,
      interaction: false,
      showScore: false,
      scoring: false,
      register: false,
      userExists: true,
      paid: true,
      scoreCount: 0,
      amount: 0,
      uid: "",
      alreadyPaid: false,
      help: false,
      currcode: "",
      curref: ""
    };
  },
  methods: {
    incAm() {
      if (this.scoring) {
        this.amount++;
      }
    },
    decAm() {
      if (this.scoring && this.amount > 0) {
        this.amount--;
      }
    },
    onkey(e) {
      console.log(e.key)
      this.redeploy(e.key);
      this.refresh(e.key);
      switch (e.key) {
        case "9": // INC
          this.incAm();
          break;
        case "8": // DEC
          this.decAm();
          break;
        case "AudioVolumeUp": // INC
          this.incAm();
          break;
        case "AudioVolumeDown": // DEC
          this.decAm();
          break;
        case "4": // HELP
          if (!this.interaction) {
            this.interaction = true;
            this.help = true;
          }
          break;
        case "5": // SHOW SCORE
          if (!this.interaction) {
            this.getScore();
            this.interaction = true;
            this.showScore = true;
          }
          break;
        case "6": // SCORING
          if (!this.interaction) {
            this.scoring = true;
            this.interaction = true;
            this.addScore();
          }
          break;
        case "2": // PAY
          if (!this.register && !this.interaction) {
            this.register = true;
            this.interaction = true;
            this.pay(false);
          } else if (this.register){
            this.pay(true)
          }
          break;
        case "1": // RESET
          this.cancel(0);
      }
    },
    async refresh(key) {
      this.curref += key;
      if (this.curref.substr(this.curref.length - 4) == "4444") {
        this.$parent.updateKey += 1;
      }
    },
    async redeploy(key) {
      this.currcode += key;
      if (this.currcode == "22554646") {
        await fetch(`/api/redeploy`)
          .then((res) => res.json())
      }
    },
    async getCard(pay=false, tm=10) {
      const uid = await fetch(`/api/card?timeout=${tm}`)
        .then((res) => res.json())
        .then((uid) => {return uid});
      this.card = true;
      const exist = await this.uidExists(uid);
      if (!exist && !pay) {
        this.userExists = false;
        return false;
      } else if (exist) {
        this.userExists = true;
      }
      return uid;
    },
    async uidExists(uid) {
      const exists = await fetch(`/api/exists?uid=${uid}`)
        .then((res) => res.json() )
        .then((exists) => {return exists} );
      return (exists === 'true');
    },
    noUser() {
      this.userExists = false;
      this.cancel(5);
    },
    cancel(timeout) {
      clearTimeout(this.tm);
      this.tm = setTimeout(() => {
        this.interaction = false;
        this.scoring = false;
        this.card = false;
        this.showScore = false;
        this.register = false;
        this.userExist = true;
        this.paid = true;
        this.scoreCount = 0;
        this.amount = 0;
        this.alreadyPaid = false;
        this.stopReader();
        this.help = false;
        this.currcode = "";
        this.curref = "";
        this.uid = "";
        this
      }, timeout*1000);
    },
    async stopReader() {
      await fetch(`/api/cardstop`);
    },
    async getUser(uid) {
      const user = await fetch(`/api/user?uid=${uid}`)
        .then((res) => res.json())
        .then((user) => {return user});
      this.checkUser(user);
      return user
    },
    async checkUser(user) {
      const date = new Date(user.date)
      let timeDiff = (Date.now() - date) / (1000*3600*24);
      if (!user.paid || timeDiff > 180) {
        this.paid = false;
        this.cancel(5);
      }
    },
    async updateUser(uid, data) {
      const res = await fetch('/api/updateuser', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({uid: uid, data: data})
      })
      return await res.json();
    },
    async getScore() {
      const uid = await this.getCard();
      if (uid) {
        const user = await this.getUser(uid);
        this.scoreCount = user.score;
        this.cancel(5);
        return;
      }
      this.cancel(5);
      return;
    },
    async addScore() {
      const uid = await this.getCard();
      if (uid) {
        const user = await this.getUser(uid);
        this.userExists = true;
        if (this.paid) {
          let newScore = this.amount + user.score;
          this.scoreCount = newScore;
          await this.updateUser(uid, {score: newScore})
          this.cancel(5);
          return;
        }
      }
      this.cancel(10);
      return;
    },
    async pay(paid) {
      if (!paid) {
        const uid = await this.getCard(true);
        this.uid = uid;
        if (await this.uidExists(uid)) {
          const user = await this.getUser(uid);
          if (!this.paid) {
            this.cancel(30);
          } else {
            this.alreadyPaid = true;
            this.cancel(5);
          }
        } else {
          this.userExists = false;
          this.paid = false;
        }
      } else {
        if (this.userExists) {
          const data = {paid: true, date: new Date(Date.now())};
          this.updateUser(this.uid, data);
          this.paid = true;
          this.cancel(5);
          return;
        } else {
          const data = {paid: true, date: new Date(Date.now()), score: 0};
          console.log(data);
          const res = await fetch('/api/adduser', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({uid: this.uid, data: data})
          })
          this.paid = true;
          this.cancel(5);
          return;
        }
      }
    }
  }
};
</script>
