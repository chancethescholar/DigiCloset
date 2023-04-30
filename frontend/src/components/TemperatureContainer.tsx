import { 
    Grid,
    GridItem,
    Card,
    CardBody,
    Text
 } from "@chakra-ui/react"
 import { useEffect, useState } from "react"

export default function TemperatureContainer() {
    const [temperature, setTemperature] = useState<null | string>(null)
    const [city, setCity] = useState<null | string>(null)
    const [state, setState] = useState<null | string>(null)

    useEffect(() => {
        async function getTemperatureLocation() {
          const tempResponse = await fetch(
            `http://127.0.0.1:8000/api/ootd/weather`
          )
      
          const tempJson = await tempResponse.json()
          setTemperature(tempJson.temperature)

          const response = await fetch(
            `http://127.0.0.1:8000/api/ootd/location`
          )
      
          const locationJson = await response.json()
          setCity(locationJson.city)
          setState(locationJson.state)
        }
        getTemperatureLocation()
      }, [temperature, city, state])
    return (
        <>
            <Card maxW="100%" m={6} bg="gray.100">
                <CardBody>
                    <Grid 
                        h="100%"
                        templateColumns='repeat(5, 1fr)'
                    >
                        <GridItem colSpan={1} ml={12}>
                          <Text fontSize='7xl' as='b'>{temperature}º</Text>
                        </GridItem>
                        <GridItem colSpan={4} mt={8} ml={155} color='gray.500'>
                          <Text fontSize='4xl'>{city}, {state}</Text>
                        </GridItem>
                    </Grid>
                </CardBody>
            </Card>
        </>
    )
}
