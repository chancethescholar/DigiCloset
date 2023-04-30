import { useState } from 'react'
import {
    HStack,
    Tag,
    TagLabel,
    TagCloseButton,
    Box
} from '@chakra-ui/react'
import { colors } from 'react-select/dist/declarations/src/theme'

export default function Filter(props: any) {
    const [typesList, setTypesList] = useState<string[]>([])
    const [colorsList, setColorsList] = useState<string[]>([])

    // handles the filter parameters
    const addType = (type: string) => {
        // if type is already in list, remove type from list
        if (typesList.includes(type))
        {
            let index = -1
            for (let i = 0; i < typesList.length; i++)
            {
                if (typesList[i] == type)
                    index = i
            }

            typesList.splice(index, 1); // 2nd parameter means remove one item only
        }
        // else add type to list
        else 
        {
            typesList.push(type)
        }

        // turn types list into string with items separated by a comma
        props.setTypes(typesList.toString())
        //console.log(typesList)
        //console.log(props.types)
    }

    const addColor = (color: string) => {
        // if color is already in list, remove color from list
        if (colorsList.includes(color))
        {
            let index = -1
            for (let i = 0; i < colorsList.length; i++)
            {
                if (colorsList[i] == color)
                    index = i
            }
    
            colorsList.splice(index, 1); // 2nd parameter means remove one item only
        }
        // else add color to list
        else 
        {
            colorsList.push(color)
        }
    
        // turn colors list into string with items separated by a comma
        props.setColors(colorsList.toString())
        //console.log(colorsList)
        //console.log(props.colors)
    }

    // show different variant for tags to indicate if it is checked or not
    const getVariantType = (check: string) => {
        if (typesList.includes(check) || colorsList.includes(check))
            return "subtle"
        else
            return "outline"
    }

    return (
        <>
            <HStack spacing={8} ml={10} mt={4} mb={4}>
            {['Dress', 'Jacket', 'Top', 'Pants', 'Shorts', 'Skirt', 'Sweater', 'Shoe'].map((type) => (
                <Tag
                as="button"
                size='lg'
                key={type}
                borderRadius='full'
                variant={getVariantType(type)}
                colorScheme='red'
                onClick={() => addType(type)}
                >
                    <TagLabel>{type}</TagLabel>
                </Tag>
            ))}
            </HStack>
            <HStack spacing={4} ml={10} mb={4}>
            {['red', 'burgundy', 'orange', 'yellow', 'green', 'blue', 'light blue', 'purple', 'pink', 'beige', 'brown', 'gray', 'black', 'white'].map((color) => (
                <Tag
                as="button"
                size='lg'
                key={color}
                borderRadius='full'
                variant={getVariantType(color)}
                colorScheme='orange'
                onClick={() => addColor(color)}
                >
                    <TagLabel>{color}</TagLabel>
                </Tag>
            ))}
            </HStack>
        </>
    )
}