import RPiMfrc522 from "rpi-mfrc522";
import { Gpio } from 'onoff';

class Reader {
  constructor() {
    console.log('Init reader')
    this.mfrc522 = new RPiMfrc522();
    this.count = 0;
    this.LED = new Gpio(4, 'out');
  }

  async run() {
    this.count = 0;
    this.LED.writeSync(1);
    let uid;
    await this.mfrc522.init();
    do {
      uid = await this.cardDetect();
    } while (uid == null && this.count < 8);
    this.LED.writeSync(0);
    return uid
  }

  async stop() {
    this.count = 100;
    return true;
  }

  async cardDetect() {
    this.count++;

    console.log("Looking for card...")
    if (!(await this.mfrc522.cardPresent())) {
      console.log('No card')
      return null;
    }

    let uid = await this.mfrc522.antiCollision();
    if (uid == null) {
      console.log('Collision')
      return null;
    }

    uid = this.uidToString(uid)

    console.log('Card detected, UID ' + uid);
    await this.mfrc522.resetPCD()
    return uid;
  }

  uidToString(uid) {
    return uid.reduce((s, b) => { return s + (b < 16 ? '0' : '') + b.toString(16); }, '');
  }
}

export default Reader;
