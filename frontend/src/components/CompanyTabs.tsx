import React from "react";

interface CompanyTabsProps {
  companies: string[];
  selected: string;
  onSelect: (c: string) => void;
}

const CompanyTabs: React.FC<CompanyTabsProps> = ({ companies, selected, onSelect }) => (
  <div className="flex gap-3 mb-6 justify-center flex-wrap">
    {["All", ...companies].map((company) => {
      const active = selected === company;
      let activeClasses = "";
      let badge = null;
      if (company === "DR Horton") {
        activeClasses = active ? "bg-blue-600 text-white shadow-lg" : "bg-blue-50 text-blue-700 hover:bg-blue-100";
        badge = <span className="inline-block w-3 h-3 rounded-full bg-blue-500 mr-2"></span>;
      } else if (company === "UnionMain Homes") {
        activeClasses = active ? "bg-cyan-600 text-white shadow-lg" : "bg-cyan-50 text-cyan-700 hover:bg-cyan-100";
        badge = <span className="inline-block w-3 h-3 rounded-full bg-cyan-500 mr-2"></span>;
      } else {
        activeClasses = active ? "bg-blue-800 text-white shadow-lg" : "bg-blue-100 text-blue-700 hover:bg-blue-200";
      }
      return (
        <button
          key={company}
          className={`px-6 py-2 rounded-full font-semibold transition-all duration-200 flex items-center ${activeClasses} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-400`}
          onClick={() => onSelect(company)}
        >
          {company !== "All" && badge}
          {company}
        </button>
      );
    })}
  </div>
);

export default CompanyTabs; 