# Group:    Margelino, Kristina Marie
#           Hizola, Alfred Luis
#           Bellen, Aila Marie
#           Labrador, Windelyn

# Information Assurance and Security
# Image and Text Based Steganography Tool using LSB (Least Significant Bit) method

from PIL import Image
# import package Pillow for image processing

# -------------------- IMAGE STEGANOGRAPHY --------------------

class ImageSteganography:
    
    @staticmethod
    def gen_data(data):
        return [format(ord(i), '08b') for i in data]

    @staticmethod
    def mod_pix(pix, data):
        datalist = ImageSteganography.gen_data(data)
        lendata = len(datalist)
        imdata = iter(pix)

        for i in range(lendata):
            pixels = [value for value in next(imdata)[:3] +
                      next(imdata)[:3] +
                      next(imdata)[:3]]

            for j in range(8):
                if datalist[i][j] == '0' and pixels[j] % 2 != 0:
                    pixels[j] -= 1
                elif datalist[i][j] == '1' and pixels[j] % 2 == 0:
                    pixels[j] = pixels[j] - 1 if pixels[j] != 0 else pixels[j] + 1

            pixels[-1] = pixels[-1] | 1 if i == lendata - 1 else pixels[-1] & ~1

            yield tuple(pixels[:3])
            yield tuple(pixels[3:6])
            yield tuple(pixels[6:9])

    @staticmethod
    def encode_image(image_path, output_path, data):
        try:
            image = Image.open(image_path, 'r')
        except Exception as e:
            print(f"Error: {e}")
            return

        if not data:
            print("Error: No data to encode.")
            return

        newimg = image.copy()
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in ImageSteganography.mod_pix(image.getdata(), data):
            newimg.putpixel((x, y), pixel)
            x = 0 if x == w - 1 else x + 1
            y += 1 if x == 0 else 0

        newimg.save(output_path)
        print(f"Message encoded and saved to: {output_path}")

    @staticmethod
    def decode_image(image_path):
        try:
            image = Image.open(image_path, 'r')
        except Exception as e:
            print(f"Error: {e}")
            return ""

        imgdata = iter(image.getdata())
        data = ""

        while True:
            pixels = [value for value in next(imgdata)[:3] +
                      next(imgdata)[:3] +
                      next(imgdata)[:3]]
            binstr = ''.join(['1' if i % 2 else '0' for i in pixels[:8]])
            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                break

        return data

# -------------------- TEXT STEGANOGRAPHY --------------------

class TextSteganography:
    
    @staticmethod
    def text_to_binary(text):
        return ''.join(format(ord(c), '08b') for c in text)

    @staticmethod
    def binary_to_text(binary):
        chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
        return ''.join(chr(int(c, 2)) for c in chars)

    @staticmethod
    def hide_message(cover_text, message):
        binary = TextSteganography.text_to_binary(message) + '00000000'
        stego_lines = []
        i = 0
        for line in cover_text.splitlines():
            if i < len(binary):
                bit = binary[i]
                if bit == '0':
                    stego_lines.append(line + ' ')  # space = 0
                else:
                    stego_lines.append(line + '\t')  # tab = 1
                i += 1
            else:
                stego_lines.append(line)
        return '\n'.join(stego_lines)

    @staticmethod
    def extract_message(stego_text):
        binary = ''
        for line in stego_text.splitlines():
            if line.endswith(' '):
                binary += '0'
            elif line.endswith('\t'):
                binary += '1'
        if '00000000' in binary:
            binary = binary[:binary.index('00000000')]
        return TextSteganography.binary_to_text(binary)

# -------------------- MAIN LOOP --------------------

def main():
    
    while True:
        print("\n:: STEGANOGRAPHY TOOL ::")
        print("[1] Image-Based Steganography")
        print("[2] Text-Based Steganography")
        print("[0] Exit")
        
        choice = input("Choose steganography type: ")

        if choice == '1':
            print("\n-- Image-Based Steganography --")
            print("[1] Encode")
            print("[2] Decode")
            print("[0] Back")
            
            action = input("Choose action: ")

            if action == '1':
                
                img_path = input("Enter path to image file: ")
                data = input("Enter the message to hide: ")
                out_path = input("Enter path to save the encoded image: ")
                
                # Pass user input values to function
                ImageSteganography.encode_image(img_path, out_path, data)

            elif action == '2':
                
                img_path = input("Enter path to image file: ")
                
                # Pass user input values to function
                result = ImageSteganography.decode_image(img_path)
                
                print("Decoded Message:", result)

            elif action == '0':
                continue
            
            else:
                print("Invalid option.")

        elif choice == '2':
            
            print("\n-- Text-Based Steganography --")
            print("[1] Encode")
            print("[2] Decode")
            print("[0] Back")
            
            action = input("Choose action: ")

            if action == '1':
                
                cover_path = input("Enter path to cover text file: ")
                message = input("Enter the message to hide: ")
                output_path = input("Enter path to save stego text: ")
                
                try:
                    with open(cover_path, 'r', encoding='utf-8') as f:
                        cover = f.read()
                    stego = TextSteganography.hide_message(cover, message)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(stego)
                    print("Message hidden successfully.")
                    
                except Exception as e:
                    print(f"Error: {e}")

            elif action == '2':
                
                stego_path = input("Enter path to stego text file: ")
                
                try:
                    with open(stego_path, 'r', encoding='utf-8') as f:
                        stego = f.read()
                    message = TextSteganography.extract_message(stego)
                    print("Decoded Message:", message)
                    
                except Exception as e:
                    print(f"Error: {e}")

            elif action == '0':
                continue
            
            else:
                print("Invalid option.")

        elif choice == '0':
            print("Exiting program")
            break

        else:
            print("Invalid Input.")

if __name__ == "__main__":
    main()