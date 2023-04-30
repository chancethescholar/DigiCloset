import { useEffect, useState } from 'react'
import NavBar from "../components/NavBar"
import TemperatureContainer from "../components/TemperatureContainer"
import {
    Box,
    Text,
    Card,
    CardBody,
    Image,
    Grid,
    GridItem,
    Stack
} from "@chakra-ui/react"

export function OOTD(props: any) {
    const [data, setData] = useState<any>(null)
    const [outfit, setOutfit] = useState<string[] | null>(null)
    const [missing, setMissing] = useState<string | null>(null)

    useEffect(() => {
      }, [outfit, missing])

    const getOOTD = async () =>
    {
        const response = await fetch(
            `http://127.0.0.1:8000/api/ootd`
          )
          
          setData(await response.json())
        
        if (data?.outfit != undefined)
        {
            setOutfit(data.outfit)
            setMissing(null)
        }

        else if (data?.missing != undefined)
        {
            setMissing(data.missing)
            setOutfit(null)
        }
    }

    console.log(outfit)

    return (
        <>
            <NavBar />
            <TemperatureContainer />
            <Stack direction={['column', 'row']} spacing='24px'>
                {outfit && outfit?.map((clothing: any) => (
                    <Card maxW='sm' key={clothing}>      
                        <CardBody key={clothing}>
                            <Image
                                src={"/" + clothing}
                                alt={clothing}
                                borderRadius='lg'
                            />
                        </CardBody>
                    </Card>
                ))}
            </Stack>

            {missing && (
                <Box 
                    position='fixed'
                    top='50%'
                    left='20%'
                    right='20%'
                >
                    <Text color='gray.500' fontSize='4xl' mt={6} >
                        Try adding more clothing to your closet. We're missing a {missing} for your outfit.
                    </Text>
                </Box>
            )}

            <Box 
                as='button'
                borderRadius='md'
                bg='red.300'
                color="white"
                px={6} 
                h={14}
                position='fixed'
                bottom='50px'
                right={["50%", "45%"]}
                onClick={getOOTD}
            >
                <Text fontSize="3xl" mt={2}>Generate</Text>
            </Box>
        </>
    )
}