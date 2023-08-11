import React, {useContext, useState, useEffect} from "react";
import { auth } from "../firebase";
import { createUserWithEmailAndPassword, User as FirebaseUser, onAuthStateChanged } from "firebase/auth";

type AuthContextType = {
    currentUser: FirebaseUser | null;
    signup: (email: string, password: string) => Promise<unknown>;
};

const AuthContext = React.createContext<AuthContextType>({
    currentUser: null,
    signup: (email: string, password: string) => createUserWithEmailAndPassword(auth, email, password),
});

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
        });

        return () => {
            unsubscribe();
        };
    }, []);

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