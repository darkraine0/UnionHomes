import React from "react";

interface TypeTabsProps {
  selected: string;
  onSelect: (type: string) => void;
}

const TypeTabs: React.FC<TypeTabsProps> = ({ selected, onSelect }) => (
  <div className="flex bg-gray-100 rounded-xl p-1 shadow-inner">
    {["Now", "Plan"].map((type) => {
      const active = selected === type;
      return (
        <button
          key={type}
          className={`relative px-6 py-3 rounded-lg font-semibold text-sm transition-all duration-300 ${
            active 
              ? "bg-white text-gray-900 shadow-md transform scale-105" 
              : "text-gray-600 hover:text-gray-800 hover:bg-gray-50"
          }`}
          onClick={() => onSelect(type)}
        >
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${
              type === "Now" 
                ? active ? "bg-green-500" : "bg-green-400" 
                : active ? "bg-purple-500" : "bg-purple-400"
            }`} />
            <span>{type}</span>
          </div>
          {active && (
            <div className={`absolute inset-0 rounded-lg border-2 ${
              type === "Now" ? "border-green-200" : "border-purple-200"
            }`} />
          )}
        </button>
      );
    })}
  </div>
);

export default TypeTabs; 