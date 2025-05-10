import './lp.css'
import { useState } from 'react'
import Message from './message'

export default function Lp() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSend = () => {
        if (input.trim()) {
            setMessages(prev => [...prev, input]);
            setInput('');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') handleSend();
    };

    return (
        <div className="lp-main">
            <div className="lp-in">
                <div className="lp-in-1">
                    {messages.length > 0 && <Message messages={messages} />}
                </div>
                <div className="lp-in-2">
                    <div className="input-bar">
                        <input
                            type="text"
                            placeholder='Enter your query here..'
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyPress}
                        />
                        <button onClick={handleSend}>▲</button>
                    </div>
                </div>
            </div>
        </div>
    );
}
