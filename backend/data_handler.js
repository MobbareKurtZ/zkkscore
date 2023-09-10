import { initializeApp } from "firebase/app";
import { getFirestore, doc, getDoc, setDoc, updateDoc } from "firebase/firestore";

class DataHandler {
  constructor() {
    const firebaseConfig = {
      apiKey: "AIzaSyCWvNywt1Gq8Kkuf0AzpGt1AN_3TEj1RfU",
      authDomain: "ztek-tv.firebaseapp.com",
      databaseURL: "https://ztek-tv-default-rtdb.europe-west1.firebasedatabase.app",
      projectId: "ztek-tv",
      storageBucket: "ztek-tv.appspot.com",
      messagingSenderId: "17721318917",
      appId: "1:17721318917:web:ae4907b56f9ecf65a3066c",
      measurementId: "G-X3MK5PJGDL"
    };

    const app = initializeApp(firebaseConfig);
    this.db = getFirestore(app);
  }

  async exists(uid) {
    let userRef = doc(this.db, "users", uid)
    const user = await getDoc(userRef);
    return user.exists();
  }

  async getUser(uid) {
    let userRef = doc(this.db, "users", uid)
    const user = await getDoc(userRef).then((res) => {
      return res.data();
    })
    console.log(user)
    return user;
  }

  async addUser(uid, data) {
    await setDoc(doc(this.db, 'users', uid), data);
  }

  async updateUser(uid, data) {
    let userRef = doc(this.db, "users", uid)
    await updateDoc(userRef, data);
  }

}

export default DataHandler
