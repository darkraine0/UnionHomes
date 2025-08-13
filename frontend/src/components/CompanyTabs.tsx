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
      } else if (company === "HistoryMaker Homes") {
        activeClasses = active ? "bg-green-600 text-white shadow-lg" : "bg-green-50 text-green-700 hover:bg-green-100";
        badge = <span className="inline-block w-3 h-3 rounded-full bg-green-500 mr-2"></span>;
      } else if (company === "K. Hovnanian Homes") {
        activeClasses = active ? "bg-orange-600 text-white shadow-lg" : "bg-orange-50 text-orange-700 hover:bg-orange-100";
        badge = <span className="inline-block w-3 h-3 rounded-full bg-orange-500 mr-2"></span>;
      } else if (company === "M/I Homes") {
        activeClasses = active ? "bg-purple-600 text-white shadow-lg" : "bg-purple-50 text-purple-700 hover:bg-purple-100";
        badge = <span className="inline-block w-3 h-3 rounded-full bg-purple-500 mr-2"></span>;
      } else if (company === "Pacesetter Homes") {
        activeClasses = active ? "bg-amber-600 text-white shadow-lg" : "bg-amber-50 text-amber-700 hover:bg-amber-100";
        badge = <span className="inline-block w-3 h-3 rounded-full bg-amber-500 mr-2"></span>;
      } else if (company === "Trophy Signature Homes") {
        activeClasses = active ? "bg-emerald-600 text-white shadow-lg" : "bg-emerald-50 text-emerald-700 hover:bg-emerald-100";
        badge = <span className="inline-block w-3 h-3 rounded-full bg-emerald-500 mr-2"></span>;
      } else {
        activeClasses = active ? "bg-blue-800 text-white shadow-lg" : "bg-blue-100 text-blue-700 hover:bg-blue-200";
        badge = <span className="inline-block w-3 h-3 rounded-full bg-blue-500 mr-2"></span>;
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