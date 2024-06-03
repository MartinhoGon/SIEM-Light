import React from "react";
import {
  Button,
  Dialog,
  DialogHeader,
  DialogBody,
  DialogFooter,
} from "@material-tailwind/react";
 
export function DefaultDialog({open, handleOpen, message, title, hideButtons }) {
 
  return (
    <>
      <Dialog open={open} handler={handleOpen} >
        <DialogHeader>{title}</DialogHeader>
        <DialogBody>
          {message}
        </DialogBody>
        <DialogFooter>
          {/* <Button
            variant="text"
            color="red"
            onClick={handleOpen}
            className="mr-1"
          >
            <span>Cancel</span>
          </Button> */}
          {!hideButtons && 
          <Button variant="gradient" color="gray" onClick={handleOpen}>
            <span>Close</span>
          </Button>}
          
        </DialogFooter>
      </Dialog>
    </>
  );
}

export default DefaultDialog