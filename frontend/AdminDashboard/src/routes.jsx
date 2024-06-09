import {
  HomeIcon,
  BellIcon,
  AdjustmentsHorizontalIcon,
  InformationCircleIcon,
  CircleStackIcon,
} from "@heroicons/react/24/solid";
import { Home, Profile, Alerts, Feeds, Notifications, Tools} from "@/pages/dashboard";
// import { SignIn, SignUp } from "@/pages/auth";

const icon = {
  className: "w-5 h-5 text-inherit",
};

export const routes = [
  {
    layout: "dashboard",
    pages: [
      {
        icon: <HomeIcon {...icon} />,
        name: "dashboard",
        path: "/home",
        element: <Home />,
      },
      {
        icon: <AdjustmentsHorizontalIcon {...icon} />,
        name: "Tools",
        path: "/tools",
        element: <Tools />,
      },
      {
        icon: <BellIcon {...icon} />,
        name: "Alerts",
        path: "/alerts",
        element: <Alerts />,
      },
      {
        icon: <CircleStackIcon {...icon} />,
        name: "Feeds",
        path: "/feeds",
        element: <Feeds />,
      }
      // {
      //   icon: <InformationCircleIcon {...icon} />,
      //   name: "notifications",
      //   path: "/notifications",
      //   element: <Notifications />,
      // },
      // {
      //   icon: <CircleStackIcon {...icon} />,
      //   name: "Profile",
      //   path: "/profile",
      //   element: <Profile />,
      // }
    ],
  }
];

export default routes;
