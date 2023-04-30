// Importing combination
import { useEffect, useState, useRef } from "react";
import { 
    Tag, 
    Card, 
    CardBody, 
    CardFooter,
    Image,
    Divider,
    ButtonGroup,
    Button,
    SimpleGrid,
    Box,
    IconButton,
    AlertDialog,
    AlertDialogBody,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogContent,
    AlertDialogOverlay,
    useDisclosure,
    Spinner,
    Center,
    useToast
} from '@chakra-ui/react'
import {DeleteIcon} from '@chakra-ui/icons'
import NavBar from '../components/NavBar'
import ClothingModal from '../components/ClothingModal'
import {AiFillEdit} from 'react-icons/ai'
import AddClothing from '../components/AddClothing'
import Filter from "../components/Filter";
 
export function Closet(props: any) {
    const [ closet, setCloset ] = useState([]);
    const { isOpen, onOpen, onClose } = useDisclosure()
    const cancelRef = useRef<HTMLButtonElement>(null);
    const toast = useToast()
    const { isOpen: isModalOpen, onOpen: onModalOpen, onClose: onModalClose } = useDisclosure()
    const [ clothing, setClothing ] = useState<any>(null)
    const [ types, setTypes ] = useState("")
    const [ colors, setColors ] = useState("")
    const [ submitting, setSubmitting ] = useState(false)

    // fetch closet data from database
    useEffect(() => {
        async function getCloset() {
          const response = await fetch(
            `http://127.0.0.1:8000/api/closet?type=${types}&colors=${colors}`
          )
      
          setCloset(await response.json())
        }
        getCloset()
      }, [closet])

    // delete clothing when delete icon on corresponding card is clicked
    const handleDelete = (c: any) =>
    {
        const requestOptions = {
            method: 'POST'
          };
        
          fetch(`http://127.0.0.1:8000/api/closet/${c.id}/delete`, requestOptions).then((response) => {
          }).then((result) => {
            // close clothing modal
            onClose()
            // show notification at bottom saying clothing item was deleted
            toast({
                title: 'Clothing item deleted.',
                status: 'success',
                duration: 5000,
                isClosable: true,
              })
          });
    }

    //console.log(isOpen)

    // split colors string from database into list
    const getColors = (c: any) =>
    {
        return c.colors?.split(",")
    }

    return (
        <div>
            <NavBar />
            {/* File input */}
            <AddClothing setSubmitting={setSubmitting}/>

            {/* Clothing modal */}
            <ClothingModal isOpen={isModalOpen} onOpen={onModalOpen} onClose={onModalClose} clothing={clothing}/>
            <Filter types={types} setTypes={setTypes} colors={colors} setColors={setColors}/>

            {submitting && (
                <Center>
                    <Spinner color='red.300' size='xl' mt={25}/>
                </Center>
            )}

            {/* Display clothing from database in grid with 3 columns */}
            {!submitting && (
                <SimpleGrid columns={3} spacing={2}>
                    {closet.map((c: any) => (
                        <Box w='100%' h='100%' key={c.id}>
                            <Card maxW='sm' key={c.id}>      
                                <CardBody>
                                    <Image
                                    src={"/" + c.image}
                                    alt={"Clothing " + c.id}
                                    borderRadius='lg'
                                    />
                                </CardBody>
                                <Divider color='gray'/>

                                <CardFooter>
                                    {/* Card footer should have clothing type and colors */}
                                    <ButtonGroup spacing='2'>
                                        {c.type != null && (
                                            <Tag size='md' key={c.id + "." + c.type} variant='solid' bg='orange.200'>
                                                {c.type}
                                            </Tag>
                                        )}
                                        {getColors(c)?.map((color: string | null) => color && (
                                            <Tag size='md' key={c.id + "." + color} variant='solid' bg='red.700'>
                                                {color}
                                            </Tag>
                                        ))}
                                        {/* Also include buttons to delete and edit*/}
                                        <IconButton mr={6} aria-label='Delete Clothing' icon={<DeleteIcon />} bg='transparent' color='gray' onClick={onOpen}/>
                                        <IconButton mr={6} aria-label='Edit Clothing' icon={<AiFillEdit />} bg='transparent' color='gray' onClick={() => {
                                            // set the correct clothing item to pass to modal
                                            setClothing(c)

                                            // open clothing modal
                                            onModalOpen()
                                        }}/>
                                    </ButtonGroup>
                                </CardFooter>
                            </Card>

                            {/* Dialog opens when delete button is clicked to confirm delete */}
                            <AlertDialog
                                isOpen={isOpen}
                                leastDestructiveRef={cancelRef}
                                onClose={onClose}
                            >
                                <AlertDialogOverlay>
                                    <AlertDialogContent>
                                        <AlertDialogHeader fontSize='lg' fontWeight='bold'>
                                        Delete Clothing
                                        </AlertDialogHeader>
                
                                        <AlertDialogBody>
                                        Are you sure? You can't undo this action afterwards.
                                        </AlertDialogBody>
                
                                        <AlertDialogFooter>
                                        <Button ref={cancelRef} onClick={onClose}>
                                            Cancel
                                        </Button>
                                        <Button bg='red.400' color='white' onClick={() => handleDelete(c)} ml={3}>
                                            Delete
                                        </Button>
                                        </AlertDialogFooter>
                                    </AlertDialogContent>
                                </AlertDialogOverlay>
                            </AlertDialog>
                        </Box>
                    ))}
                </SimpleGrid>
            )}
        </div>
    );
}
