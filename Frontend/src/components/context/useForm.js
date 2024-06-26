import React,{useState} from "react";
import { useContext,createContext } from "react";

export const context=React.createContext()
export const   FormProvide=context.Provider
export default function useForm(){
    return useContext(context)
}
