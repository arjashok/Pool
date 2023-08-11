import React, {useRef} from "react";
import { Form, Button, Card } from "react-bootstrap";

export default function Signup() {
    const emailRef = useRef<HTMLInputElement>(null);
    const passwordRef = useRef<HTMLInputElement>(null);
    const passwordConfirmRef = useRef<HTMLInputElement>(null);
    return (
        <div>
            <Card>
                <Card.Body>
                    <h2 className="text-center mb-4">Sign Up</h2>
                    <Form>
                        <Form.Group className="mt-2" id="email">
                            <Form.Label> Email </Form.Label>
                            <Form.Control type="email" ref = {emailRef} required />
                        </Form.Group>
                        <Form.Group className="mt-2" id="password">
                            <Form.Label> Password </Form.Label>
                            <Form.Control type="password" ref = {passwordRef} required />
                        </Form.Group>
                        <Form.Group className="mt-2" id="password-confirm">
                            <Form.Label> Password Confirmation </Form.Label>
                            <Form.Control type="password" ref = {passwordConfirmRef} required />
                        </Form.Group>
                        <Button className="w-100 mt-4" type="submit">Sign Up</Button>
                    </Form>
                </Card.Body>
            </Card>
            <div className="w-100 text-center mt-2">
                Already have an account? Log in
            </div>
        </div>
    );
}