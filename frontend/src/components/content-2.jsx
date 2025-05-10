import { useState } from 'react';

const tabOptions = [
    "Best Response",
    "Generation",
  "Reflection",
  "Ranking",
  "Evolution",
  "Proximity",
  "Meta Review",
  "Resources"
];

export default function Content2() {
  const [activeTab, setActiveTab] = useState("Final Response");

  const renderContent = () => {
    switch (activeTab) {
    case "Final Response":
        default:
          return <p>This is the Final Response (default) content.</p>;
      case "Generation":
        return <p>This is the Generation content.</p>;
      case "Reflection":
        return <p>This is the Reflection content.</p>;
      case "Ranking":
        return <p>This is the Ranking content.</p>;
      case "Evolution":
        return <p>This is the Evolution content.</p>;
      case "Proximity":
        return <p>This is the Proximity content.</p>;
      case "Meta Review":
        return <p>This is the Meta Review content.</p>;
      case "Resources":
        return <p>This is the Resources.</p>;
    }
  };

  return (
    <div className="content-2">
      <div className="tab-container">
        {tabOptions.map(tab => (
          <div
            key={tab}
            className={`tab-item ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </div>
        ))}
      </div>
      <div className="tab-content">
        {renderContent()}
      </div>
    </div>
  );
}
