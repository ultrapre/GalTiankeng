/*
source:
http://wiki.wareya.moe/Lucifen%20Library

Engine:
Lucifen

Game:
[Navel] 俺たちに翼はない AfterStory - Limited Edition -

Scripts:
*.tob

Make:
g++ -o tobRead.exe tobRead.cpp

Use Sample:
tobR.exe M:\ZUBASA\SCRIPT\s04_13a.tob>>s04_13a.txt

*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include <set>
#include <map>

std::map<uint32_t, std::string> map; // resume table?
std::set<uint32_t> set; // resume table?

bool is_upper_jis_surrogate(int c)
{
    return (c >= 0x80 and c <= 0xA1) or (c >= 0xE0 and c <= 0xFF);
}

int main(int argc, char ** argv)
{
    //int strings = 0;
    for(int i = 0; i < argc; i++)
    {
        map.clear();
        set.clear();
        
        auto f = fopen(argv[i], "rb");
        if(!f) continue;
        char magic[4];
        int n = fread(magic, 1, 4, f);
        if(n != 4 or strncmp(magic, "TOB0", 4) != 0) continue;
        
        //puts(argv[i]);
        
        uint32_t header_size;
        uint32_t header_elements;
        fread(&header_size, 4, 1, f);
        fread(&header_elements, 4, 1, f);
        
        for(int j = 0; j < header_elements; j++)
        {
            uint8_t size;
            fread(&size, 1, 1, f);
            
            char * text = (char *)malloc(size-4);
            fread(text, 1, size-4, f);
            
            uint32_t value;
            fread(&value, 4, 1, f);
            map[value] = text;
            
            free(text);
        }
        if(ftell(f) != header_size+4)
        {
            puts("desynchronized"), puts(argv[i]);
            exit(0);
        }
        
        
        uint32_t table_size;
        uint32_t table_elements;
        fread(&table_size, 4, 1, f);
        fread(&table_elements, 4, 1, f);
        uint32_t table_end = table_size + header_size + 4;
        while(ftell(f) < table_end)
        {
            //printf("Header at %08X\n", ftell(f));
            uint32_t word;
            fread(&word, 4, 1, f);
            set.insert(word);
        }
        
        fseek(f, table_end, SEEK_SET);
        
        std::string text = "";
        uint32_t start = ftell(f);
        while(1)
        {
            uint32_t location = ftell(f);
            
            // I have absolutely no idea if these are correct.
            auto c = fgetc(f);
            bool closefile = feof(f) or ferror(f) or c < 0;
            if(closefile)
            {
                if(text != "")
                {
                    printf("%s\n", text.data());
                }
                break;
            }
            if(c == 0x5B) // STOP MAKING INHERENTLY ASCII INCOMPATIBLE FORMATS REEEEEEEEEEEEEEEEEEEEEEE
            {
                if(text != "")
                {
                    //printf("%08X \"%s\"\n", start, text.data());
                    printf("%s\n", text.data());
                }
                text = "";
                
                start = ftell(f);
            }
            else if(c == 0x20)
            {
                fseek(f, 4, SEEK_CUR);
                continue;
            }
            else if(c == 0x01)
            {
                uint32_t length;
                fread(&length, 4, 1, f);
                if(length < 4)
                {
                    printf("mayday in op 01 at %08X in %s\n", location, argv[i]);
                    exit(0);
                }
                fseek(f, length-4, SEEK_CUR);
                continue;
            }
            else if(c == 0x03)
            {
                // I have no idea how this works. Don't blame me if it breaks.
                uint16_t unknown1;
                fread(&unknown1, 2, 1, f);
                if(unknown1 > 0xFF)
                {
                    printf("mayday 1 in op 03 at %08X in %s\n", location, argv[i]);
                    exit(0);
                }
                fseek(f, unknown1+1, SEEK_CUR);
                
                uint16_t unknown2;
                fread(&unknown2, 2, 1, f);
                if(unknown2 < 2)
                {
                    printf("mayday 2 in op 03 at %08X in %s\n", location, argv[i]);
                    exit(0);
                }
                unknown2 -= 2;
                fseek(f, unknown2-2, SEEK_CUR);
                
                uint32_t unknown3;
                fread(&unknown3, 4, 1, f);
                if(unknown3 < 4)
                {
                    printf("mayday 3 in op 03 at %08X in %s\n", location, argv[i]);
                    exit(0);
                }
                fseek(f, unknown3-4, SEEK_CUR);
                continue;
            }
            else if(c == 0x02)
            {
                // I have no idea how this works. Don't blame me if it breaks.
                fseek(f, 8, SEEK_CUR);
                
                uint32_t unknown1;
                fread(&unknown1, 4, 1, f);
                if(unknown1 < 4)
                {
                    printf("mayday 2 in op 03 at %08X in %s\n", location, argv[i]);
                    exit(0);
                }
                fseek(f, unknown1-4, SEEK_CUR);
                continue;
            }
            else if(c == 0x73)
            {
                uint32_t length;
                fread(&length, 4, 1, f);
                if(length > 0x0000FFFF)
                {
                    printf("mayday 1 in op 73 at %08X in %s\n", location, argv[i]);
                    exit(0);
                }
                fseek(f, length+1, SEEK_CUR);
                fread(&length, 4, 1, f);
                if(length < 4)
                {
                    printf("mayday 2 in op 73 at %08X in %s\n", location, argv[i]);
                    exit(0);
                }
                fseek(f, length-4, SEEK_CUR);
                continue;
            }
            else if(is_upper_jis_surrogate(c))
            {
                bool intext = true;
                while(intext)
                {
                    text += c;
                    if(is_upper_jis_surrogate(c))
                        text += fgetc(f);
                    c = fgetc(f);
                    if(c == 0x5B)
                        intext = false;
                }
            }
            else if(c == 0)
            {
                if(fgetc(f) >= 0)
                {
                    printf("unknown operation %02X at %08X in %s\n", c, location, argv[i]);
                    exit(0);
                }
                else
                    break;
            }
            else
            {
                printf("unknown operation %02X at %08X in %s\n", c, location, argv[i]);
                //exit(0);
                break;
            }
        }
        
        fclose(f);
    }
    //printf("Total strings: %d\n", strings);
    //for(auto &[k, v] : examples)
    //{
    //    printf("%08X: %s\n", k, v.data());
    //}
}