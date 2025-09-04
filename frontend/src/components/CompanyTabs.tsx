import React from "react";
import { getCompanyColor } from "../utils/colors";

interface CompanyTabsProps {
  companies: string[];
  selected: string;
  onSelect: (c: string) => void;
}

const CompanyTabs: React.FC<CompanyTabsProps> = ({ companies, selected, onSelect }) => {
  const getTabColors = (company: string, isActive: boolean) => {
    if (company === "All") {
      return {
        activeClasses: isActive ? "bg-gray-800 text-white shadow-lg" : "bg-gray-100 text-gray-700 hover:bg-gray-200",
        badge: null
      };
    }
    
    const color = getCompanyColor(company);
    // Convert hex to RGB for opacity
    const hexToRgb = (hex: string) => {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
      } : null;
    };
    
    const rgb = hexToRgb(color);
    if (!rgb) {
      return {
        activeClasses: isActive ? "bg-gray-800 text-white shadow-lg" : "bg-gray-100 text-gray-700 hover:bg-gray-200",
        badge: <span className="inline-block w-3 h-3 rounded-full bg-gray-500 mr-2"></span>
      };
    }
    
    const activeClasses = isActive 
      ? `text-white shadow-lg` 
      : `text-gray-700 hover:bg-opacity-20`;
    
    const bgColor = isActive ? color : `${color}20`;
    const textColor = isActive ? 'white' : color;
    
    return {
      activeClasses: `${activeClasses}`,
      badge: <span className="inline-block w-3 h-3 rounded-full mr-2" style={{ backgroundColor: color }}></span>,
      style: {
        backgroundColor: bgColor,
        color: textColor
      }
    };
  };

  return (
    <div className="flex gap-3 mb-6 justify-center flex-wrap">
      {["All", ...companies].map((company) => {
        const active = selected === company;
        const { activeClasses, badge, style } = getTabColors(company, active);
        
        return (
          <button
            key={company}
            className={`px-6 py-2 rounded-full font-semibold transition-all duration-200 flex items-center ${activeClasses} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-400`}
            style={style}
            onClick={() => onSelect(company)}
          >
            {company !== "All" && badge}
            {company}
          </button>
        );
      })}
    </div>
  );
};

export default CompanyTabs; 