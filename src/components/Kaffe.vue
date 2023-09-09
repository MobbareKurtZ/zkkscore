<template>
  <div v-if="score || showScore" class="kaffe-wrapper">
    <div class="kaffe-score" v-if="score">
      <div v-if="!card">
        <img src="@/assets/scan.gif" alt="scan" class="scan" />
        <h3>Select cups amount on keypad</h3>
        <h1>{{ amount }} cups</h1>
        <h2>Scan card after the correct amount is selected</h2>
      </div>

      <div v-if="card && !register">
        <h1>{{ amount }} cups registered!</h1>
        <font-awesome-icon :icon="['fas', 'mug-hot']" size="6x" />
        <h2>Your score is {{ scoreCount }}</h2>
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
      amount: 0,
      score: false,
      scoring: false,
      showScore: false,
      scoreCount: 0,
      card: false,
      register: false,
      tm: null,
      paytime: false
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
    reset(timeout) {
      clearTimeout(this.tm);
      this.tm = setTimeout(
        function () {
          this.score = false;
          this.amount = 0;
          this.scoreCount = 0;
          this.card = false;
          this.scoring = false;
          this.showScore = false;
          this.register = false;
          this.paytime = false;
        }.bind(this),
        timeout
      );
    },
    stop() {
      clearTimeout(this.tm);
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
          if (!this.scoring) {
            console.log("test")
            this.getScore();
            this.showScore = true;
          }
          break;
        case "6": // SCORING
          if (!this.showScore) {
            this.scoring = true;
            this.score = true;
            this.addScore();
          }
          break;
        case "2": // PAY
          if (this.register) {
            this.pay();
          }
          break;
        case "1": // RESET
          this.reset(0);
      }
    },
    async getCard() {
      this.reset(15000);
      const res = await fetch('/api/card');
      console.log(res)
      const uid = res.json();
      if (uid != null) {
        this.card = true;
      } else {
        this.reset(0);
      }
      return uid;
    },
    async getUser(uid) {
      console.log("aaaaaaaaaaaaaaaaaaaaaa")
      const res = await fetch(`/api/user?uid=${uid}`);
      console.log("dksjdksjdsj")
      console.log(res.json())
      const user = res.json();
      return user
    },
    async checkUser(user) {
      const date = new Date(user.date)
      let timeDiff = (Date.now() - date) / (1000*3600*24);
      if (!user) {
        this.register = true;
        this.stop();
      } else if (!user.paid || timediff > 180) {
        this.pay = true;
        this.stop();
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
      console.log(uid)
      if (uid) {
        const user = await this.getUser(uid);
        console.log(user)
        this.scoreCount = user.score;
        this.reset(4000);
      }
    },
    async addScore() {
      const uid = await this.getCard();
      if (uid) {
        const user = await this.getUser(uid);
        if (!user.paid) {
          this.register = true;
          this.stop();
        } else {
          let newScore = this.amount + user.score;
          this.updateUser(uid, {score: newScore});
          this.reset(4000);
        }
      }
    },
    async pay() {
      const uid = await this.getCard();
      this.reset();
    },
  },
};
</script>
