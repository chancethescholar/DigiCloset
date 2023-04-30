import { useState } from 'react'
import {
    Center,
    Heading,
    Box,
    Drawer,
    DrawerOverlay,
    DrawerBody,
    DrawerContent,
    SimpleGrid,
    useDisclosure,
    DrawerHeader,
    IconButton,
    Link,
    LinkBox
  } from '@chakra-ui/react';
  import {
    HamburgerIcon,
  } from '@chakra-ui/icons';
  import { Link as DomLink, useLocation} from 'react-router-dom'

  export default function NavBar() {
    const { isOpen, onOpen, onClose } = useDisclosure()
    const location = useLocation()
    const [closetLink, setClosetLink] = useState("transparent")
    const [ootdLink, setOOTDLink] = useState("transparent")

    

    return (
        <>
          <SimpleGrid columns={2} spacing='0px' mb={6} position="sticky" top={0} zIndex={1}>
              <Box bg='red.400' height='100px'>
                <Heading as='h2' size='2xl' color="white">
                  <IconButton mt={7} ml={6} aria-label='Menu' icon={<HamburgerIcon w={10} h={10} />} bg='red.400' color='white' onClick={onOpen}/>
                </Heading>
              </Box>
              <Box bg='red.400' height='100px'>
                <Heading mt={6} mr={8} textAlign={"right"} as='h2' size='2xl' color="white">
                  DigiCloset
                </Heading>
              </Box>
          </SimpleGrid>
          <Drawer placement='left' onClose={onClose} isOpen={isOpen}>
            <DrawerOverlay />
            <DrawerContent>
              <DrawerHeader borderBottomWidth='1px'>Menu</DrawerHeader>
              <DrawerBody>
                <LinkBox as='article' maxW='sm' p='5' borderWidth='1px' rounded='md' mt={4} mb={4}>
                  <Link as={DomLink} to='/closet'>Closet</Link>
                </LinkBox>
                <LinkBox as='article' maxW='sm' p='5' borderWidth='1px' rounded='md'>
                  <Link as={DomLink} to='/ootd'>OOTD</Link>
                </LinkBox>
              </DrawerBody>
            </DrawerContent>
          </Drawer>
        </>
  )
}