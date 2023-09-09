<template>
  <div v-if="interaction" class="kaffe-wrapper">
    <div class="kaffe-score" v-if="scoring">
      <div v-if="!card">
        <img src="@/assets/scan.gif" alt="scan" class="scan" />
        <h3>Select cups amount on keypad</h3>
        <h1>{{ amount }} cups</h1>
        <h2>Scan card after the correct amount is selected</h2>
      </div>

      <div v-if="card && !register">
        <h1>{{ amount }} cups registered!</h1>
        <font-awesome-icon :icon="['fas', 'mug-hot']" size="6x" />
        <h2>Your score is {{ newScore }}</h2>
      </div>

      <div v-if="card && register">
        <h1>Looks like you haven't paid for this half-year!</h1>
        <img src="@/assets/qr.png" alt="scan" id="qr" />
        <h2>Please pay, then press the pay button to continue!</h2>
        <h3>Press the X if you wish to cancel!</h3>
      </div>
    </div>

    <div class="kaffe-show-score" v-if="showScore">
      <div v-if="!card">
        <img src="@/assets/scan.gif" alt="scan" class="scan" />
        <h2>Scan card to show your score</h2>
      </div>

      <div v-if="(card && !register) || scoreCount != 0">
        <h2>Your score is {{ scoreCount }}</h2>
        <font-awesome-icon :icon="['fas', 'mug-hot']" size="6x" />
      </div>

      <div v-if="card && register && scoreCount == 0">
        <h1>You don't have any score!</h1>
        <h2>Please try to pay first by scoring some coffee.</h2>
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
      amount: 0,
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
      switch (e.key) {
        case "AudioVolumeUp": // INC
          this.incAm();
          break;
        case "AudioVolumeDown": // DEC
          this.decAm();
          break;
        case "5": // SHOW SCORE
          this.getScore();
          this.interaction = true;
          this.showScore = true;
          break;
        case "6": // SCORING
          this.scoring = true;
          this.interaction = true;
          this.addScore();
          break;
        case "2": // PAY
          break;
        case "1": // RESET
      }
    },
    async getCard() {
      const res = await fetch('/api/card');
      const uid = res.json();
      this.card = true;
      const exists = await fetch(`/api/exists?uid=${uid}`).then((res)=>{return res.json()});
      if (!exists) {
        this.noUser();
      }
      return uid;
    },
    noUser() {
      this.register = true;
      this.cancel(60);
    },
    reset(timeout) {
      clearTimeout(this.tm);
      this.tm = setTimeout(() => {
        this.interaction = false;
        this.scoring = false;
        this.card = false;
        this.showScore = false;
        this.register = false;
      }.bind(this), timeout*1000);
    },
    async getUser(uid) {
      const res = await fetch(`/api/user?uid=${uid}`);
      const user = res.json();
      this.checkUser(user);
      return user
    },
    async checkUser(user) {
      const date = new Date(user.date)
      let timeDiff = (Date.now() - date) / (1000*3600*24);
      if (!user.paid || timediff > 180) {
        this.noUser();
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
      const user = await this.getUser(uid);
      this.scoreCount = user.score;
      this.cancel(5);
    },
    async addScore() {
      const uid = await this.getCard();
      const user = await this.getUser(uid);
      let newScore = this.amount + user.score;
      await this.updateUser(uid, {score: newScore})
      this.cancel(5);
    }
  }
};
</script>
