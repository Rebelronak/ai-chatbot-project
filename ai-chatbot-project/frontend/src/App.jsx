import React from "react";
import Chatbot from "./components/Chatbot";
import "./styles/Chatbot.scss";

const App = () => {
  return (
    <div className="app-container">
      <header>
        <h1>AI Chatbot by Ronak Kanani</h1>
      </header>
      <main>
        <Chatbot />
      </main>
      <footer>
        <p>© 2025 - Created by Ronak Kanani</p>
      </footer>
    </div>
  );
};

export default App;