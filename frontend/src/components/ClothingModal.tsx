import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    Button,
    Image,
    Grid,
    GridItem,
    FormControl,
    Spacer,
    Flex,
    useToast
  } from '@chakra-ui/react'
  import Select from 'react-select'
  import { Formik, Field } from 'formik';

  export default function ClothingModal(props: any) {
    const toast = useToast();

    const getDefaultColors = (colors: string | null) => {
      if (colors != null)
      {
        let defaultColors = []
        let colorArray = colors?.split(",")
        for (let i = 0; i < colorArray?.length; i++)
        {
          defaultColors.push({value: colorArray[i], label: colorArray[i]} ,)
        }
        return defaultColors
      }

      return null
    }

    //console.log(props.isOpen)
    const typeOptions = [
      { value: 'Dress', label: 'Dress' },
      { value: 'Jacket', label: 'Jacket' },
      { value: 'Top', label: 'Top' },
      { value: 'Shorts', label: 'Shorts' },
      { value: 'Pants', label: 'Pants' },
      { value: 'Shoe', label: 'Shoe' },
      { value: 'Skirt', label: 'Skirt' },
      { value: 'Sweater', label: 'Sweater' },
    ];

    const colorOptions = [
      { value: 'red', label: 'red' },
      { value: 'burgundy', label: 'burgundy' },
      { value: 'orange', label: 'orange' },
      { value: 'yellow', label: 'yellow' },
      { value: 'green', label: 'green' },
      { value: 'blue', label: 'blue' },
      { value: 'light blue', label: 'light blue' },
      { value: 'purple', label: 'purple' },
      { value: 'pink', label: 'pink' },
      { value: 'black', label: 'black' },
      { value: 'beige', label: 'beige' },
      { value: 'brown', label: 'brown' },
      { value: 'gray', label: 'gray' },
      { value: 'white', label: 'white' },
    ];

    return (
      <>  
        <Modal isOpen={props.isOpen} onClose={props.onClose} size="lg">
          <ModalOverlay />
          <ModalContent>
            <Formik
              initialValues={{ type: {value: props.clothing?.type, label: props.clothing?.type}, colors: getDefaultColors(props.clothing?.colors) }}
              onSubmit={(values, { setSubmitting }) => {
                //console.log(values.colors)
                let colors: string | null = ""
                if (values.colors != null)
                {
                  for (let i = 0; i < values.colors.length; i++)
                  {
                    if (i == values.colors.length-1)
                      colors += values.colors[i].value
                    else
                      colors += values.colors[i].value + ","
                  }
                }

                if (colors.length == 0)
                  colors = null
                
                //console.log(values.type.value)
                console.log(colors)
                const requestOptions = {
                  method: 'POST',
                  headers: { 
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ type: values.type.value, colors: colors, image:props.clothing?.image })
                };

                fetch(`http://127.0.0.1:8000/api/closet/${props.clothing?.id}/update`, requestOptions).then((response) => {
                  }).then((result) => {
                    //console.log(result)
                    toast({
                      title: 'Clothing item updated.',
                      status: 'success',
                      duration: 5000,
                      isClosable: true,
                    })
                    props.onClose()
                  });
              }}
            >
              {({
                values,
                errors,
                touched,
                handleChange,
                handleBlur,
                handleSubmit,
                isSubmitting,
                setFieldValue
                /* and other goodies */
              }) => (
                <form onSubmit={handleSubmit}>
            <ModalHeader m={6}>Update Clothing</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <FormControl>
                <Grid
                  h='100%'
                  templateColumns='repeat(9, 1fr)'
                  gap={4}
                  ml={6}
                  mr={6}
                >
                  <GridItem colSpan={4} rowSpan={10} bg='transparent'>
                    <Image
                      src={"/" + props.clothing?.image}
                      alt={"Clothing " + props.clothing?.id}
                      borderRadius='lg'
                    />
                  </GridItem>
                  <GridItem colSpan={2} bg='transparent' mt={10}>
                    Type
                  </GridItem>
                  <GridItem colSpan={3} bg='transparent' mb={8} mt={10}>
                    <Select name='type' options={typeOptions} defaultValue={props.clothing?.type} value={values.type} onChange={(e: any) => {
                        console.log(e.value)
                        setFieldValue(`type`,{value: e.value, label: e.value})
                      }}/>
                  </GridItem>
                  <GridItem colSpan={2} bg='transparent'>
                    Color(s)
                  </GridItem>
                  <GridItem colSpan={3} bg='transparent'>
                    <Select name='colors' options={colorOptions} defaultValue={getDefaultColors(props.clothing?.colors)} isMulti={true} value={values.colors} onChange={e => {
                        let value: string | null = ""
                        console.log(e.length)
                        for (let i = 0; i < e.length; i++)
                        {
                          if (i == e.length-1)
                            value += e[i].value
                          else
                            value += e[i].value + ","
                        }
                        if (value == "")
                          value = null
                        console.log(value)
                        setFieldValue(`colors`, getDefaultColors(value))
                      }}/>
                  </GridItem>
                </Grid>
              </FormControl>
            </ModalBody>
            <ModalFooter>
              <Button bg='red.200' color='white' mr={6} mb={6} size='lg' onClick={props.onClose}>
                Close
              </Button>
              <Button bg='red.400' color='white' mr={6} mb={6} size='lg' type='submit'>Update</Button>
            </ModalFooter>
            </form>
              )}
            </Formik>
          </ModalContent>
        </Modal>
      </>
    )
  }