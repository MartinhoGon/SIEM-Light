import {
  BellAlertIcon,
  CircleStackIcon,
  BellIcon,
} from "@heroicons/react/24/solid";

export const statisticsCardsData = [
  {
    color: "gray",
    icon: BellAlertIcon,
    title: "Alerts",
    value: "53",
    footer: {
      color: "text-green-500",
      // value: "+55%",
      label: "Uncheck Alerts",
    },
  },
  {
    color: "gray",
    icon: BellIcon,
    title: "Total Alerts",
    value: "3,462",
    footer: {
      color: "text-red-500",
      label: "Total of alerts registered",
    },
  },
  {
    color: "gray",
    icon: CircleStackIcon,
    title: "Feeds",
    value: "2",
    footer: {
      color: "text-green-500",
      label: "Total feeds consumed",
    },
  }
];

export default statisticsCardsData;
