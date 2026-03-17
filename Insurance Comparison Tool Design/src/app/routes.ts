import { createBrowserRouter } from "react-router";
import { Home } from "./pages/Home";
import { Shortlist } from "./pages/Shortlist";
import { Compare } from "./pages/Compare";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Home,
  },
  {
    path: "/shortlist",
    Component: Shortlist,
  },
  {
    path: "/compare",
    Component: Compare,
  },
]);
