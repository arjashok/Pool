import React, {useContext, useState, useEffect} from "react";
import { auth } from "../firebase";
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, User, onAuthStateChanged, signOut, sendPasswordResetEmail, 
    updateEmail, updatePassword, reauthenticateWithCredential, EmailAuthProvider } from "firebase/auth";

type AuthContextType = {
    currentUser: User | null;
    signup: (email: string, password: string) => Promise<unknown>;
    login: (email: string, password: string) => Promise<unknown>;
    logout: () => Promise<unknown>;
    resetPassword: (email: string) => Promise<unknown>;
    emailUpdate: (email: string) => Promise<unknown>;
    passwordUpdate: (oldPassword: string, newPassword: string) => Promise<unknown>;
};

const AuthContext = React.createContext<AuthContextType>({
    currentUser: auth.currentUser,
    signup: (email: string, password: string) => createUserWithEmailAndPassword(auth, email, password),
    login: (email: string, password: string) => signInWithEmailAndPassword(auth, email, password),
    logout: () => signOut(auth),
    resetPassword: (email: string) => sendPasswordResetEmail(auth, email),
    emailUpdate: (email: string) => updateEmail(auth.currentUser!, email),
    passwordUpdate: (oldPassword: string, newPassword: string) => updatePassword(auth.currentUser!, newPassword),
});

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [currentUser, setCurrentUser] = useState<User | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    async function signup(email: string, password: string){
        return await createUserWithEmailAndPassword(auth, email, password);
    }

    async function login(email: string, password: string){
        return await signInWithEmailAndPassword(auth, email, password)
    }

    async function logout(){
        return await signOut(auth);
    }

    async function resetPassword(email: string){
        return await sendPasswordResetEmail(auth, email);
    }

    async function emailUpdate(email: string){
        await updateEmail(currentUser!, email);
    }

    async function passwordUpdate(oldPassword: string, newPassword: string){
        const cred = EmailAuthProvider.credential(currentUser!.email!, oldPassword);
        await reauthenticateWithCredential(currentUser!, cred).then(async () => {
            await updatePassword(currentUser!, newPassword);
        }).catch((error) => {
            console.log(error);
        });
    }
    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, user => {
            setCurrentUser(user);
            setLoading(false);
        });

        return () => {
            unsubscribe();
        };
    }, []);

    const value = {
        currentUser,
        signup,
        login,
        logout,
        resetPassword,
        passwordUpdate,
        emailUpdate
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
}