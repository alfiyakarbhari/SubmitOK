import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";


const firebaseConfig = {
  apiKey: "AIzaSyBPSsAdFhMsBneNM05KLnUVlKT-MiqcPNM",
  authDomain: "submitok-cbbd8.firebaseapp.com",
  projectId: "submitok-cbbd8",
  storageBucket: "submitok-cbbd8.firebasestorage.app",
  messagingSenderId: "514245672112",
  appId: "1:514245672112:web:8f2845bea8c7ba3d1a8f75",
  measurementId: "G-SFEV3RTYB7"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
