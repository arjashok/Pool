import React, {useContext, useState, useEffect} from "react";
import { auth } from "../firebase";
import { createUserWithEmailAndPassword, User as FirebaseUser, onAuthStateChanged } from "firebase/auth";

const AuthContext = React.createContext({});

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [currentUser, setCurrentUser] = useState<FirebaseUser | null>(null);;

    function signup(email: string, password: string){
        return createUserWithEmailAndPassword(auth, email, password);
    }

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, user => {
            setCurrentUser(user);
        })

        return unsubscribe;
    }, [])
    onAuthStateChanged(auth, user => {
        setCurrentUser(user);
    })

    const value = {
        currentUser,
        signup
    };
    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}