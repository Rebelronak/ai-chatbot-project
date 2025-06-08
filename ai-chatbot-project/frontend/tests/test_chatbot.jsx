import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import Chatbot from "../src/components/Chatbot";

describe("Chatbot Component", () => {
    test("renders input and button", () => {
        render(<Chatbot />);
        const inputElement = screen.getByPlaceholderText("Type your message...");
        const buttonElement = screen.getByText("Send");
        expect(inputElement).toBeInTheDocument();
        expect(buttonElement).toBeInTheDocument();
    });

    test("sends a message and displays bot response", async () => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                json: () => Promise.resolve({ response: "Hi there!" }),
            })
        );

        render(<Chatbot />);
        const inputElement = screen.getByPlaceholderText("Type your message...");
        const buttonElement = screen.getByText("Send");

        fireEvent.change(inputElement, { target: { value: "hello" } });
        fireEvent.click(buttonElement);

        const botResponse = await screen.findByText("Bot: Hi there!");
        expect(botResponse).toBeInTheDocument();
    });
});