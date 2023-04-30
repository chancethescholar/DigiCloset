import "@fontsource/crafty-girls"
import "@fontsource/cambay"
import { ChakraProvider } from '@chakra-ui/react'
import { Routes, Route, useNavigate, Navigate } from "react-router-dom";
import "./App.css";
import {
  Closet,
  OOTD
} from "./pages";
import theme from './theme'

export default function App() {
  return (
    <div>
      <ChakraProvider theme={theme}>
        <Routes>
          <Route path="/" element={<Closet />} />
          <Route path="/closet" element={<Closet />} />
          <Route path="/ootd" element={<OOTD />} />
        </Routes>
        </ChakraProvider>
    </div>
  );
}