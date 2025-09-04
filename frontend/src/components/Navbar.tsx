import { Link } from "react-router-dom";
import { Fragment } from "react/jsx-runtime";

const Navbar = () => (
  <Fragment>
    <div className="bg-gradient-to-r from-blue-600 to-cyan-400 shadow-lg">
      <nav className="container mx-auto py-4 px-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link to="/" className="text-2xl font-extrabold text-white tracking-tight select-none cursor-pointer">
            MarketMap Homes
          </Link>
        </div>
        <div className="flex gap-2">
          <Link to="/">
            <button
              className="px-4 py-2 rounded-xl bg-white text-blue-600 font-bold shadow hover:bg-blue-50 focus-visible:outline focus-visible:ring-2 focus-visible:ring-blue-400 transition bg-[#0078fff]"
              type="button"
            >
              Communities
            </button>
          </Link>
          <Link to="/dashboard">
            <button
              className="px-4 py-2 rounded-xl bg-white text-cyan-600 font-bold shadow hover:bg-cyan-100 focus-visible:outline focus-visible:ring-2 focus-visible:ring-cyan-400 transition"
              type="button"
            >
              All Plans
            </button>
          </Link>
        </div>
      </nav>
    </div>
  </Fragment>
);

export default Navbar;
