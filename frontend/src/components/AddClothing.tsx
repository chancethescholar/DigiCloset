import { useState, useRef } from 'react'
import {
    Box,
    useToast,
    useDisclosure
} from "@chakra-ui/react"
import {
    AddIcon
} from '@chakra-ui/icons';
import ClothingModal from "./ClothingModal";

export default function AddClothing(props: any) {
    const inputFile = useRef<HTMLInputElement | null>(null)
    //const [fileName, setFileName] = useState<string | null>(null)
    const toast = useToast()
    const { isOpen: isModalOpen, onOpen: onModalOpen, onClose: onModalClose } = useDisclosure()
    const [clothing, setClothing] = useState<any>(null)

    const onAddClick = () => {
        inputFile.current?.click();
      }
  
      const onChangeFile = (event: any) => {
        event.stopPropagation();
        event.preventDefault();

        let fileUpload = event.target.files[0];
        let fileName = fileUpload?.name
        //console.log(fileUpload.name);
        //setFileName(fileUpload.name); 
  
        console.log(fileName)
  
        const requestOptions = {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ path: fileName })
        };
  
        console.log("file name: " + fileName)
        props.setSubmitting(true)

        fetch(`http://127.0.0.1:8000/api/closet/add`, requestOptions).then((response) => {
          return response.json();
        }).then((result) => {
          //console.log(result)
          toast({
            title: 'Clothing item added.',
            status: 'success',
            duration: 5000,
            isClosable: true,
          })
          setClothing(result)
          onModalOpen()
          props.setSubmitting(false)
        });
      }

    return (
        <>
            <ClothingModal isOpen={isModalOpen} onOpen={onModalOpen} onClose={onModalClose} clothing={clothing}/>
            <input type='file' id='file' accept="image/*" ref={inputFile} style={{display: 'none'}} onChange={onChangeFile}/>
            <Box 
                position='fixed'
                bottom='40px'
                right={['16px', '40px']}
                zIndex={1}
                as='button'
                onClick={onAddClick}
                style={{ borderRadius: "50%" }}
                bg='red.400'
                h={20}
                w={20}
            >
              <AddIcon color="white" w={16} h={16} />
            </Box>
        </>
    )
}