"""
GAMEZILLA MEGA COLLECTION - Shareware Program List Generator V2
Generates 500 "programs" with hidden message support
Updated to include V5 and V6
"""

import random


class SharewareGeneratorV2:
    """Generates authentic-sounding 1995-1998 shareware program names"""

    def __init__(self, seed=None):
        if seed:
            random.seed(seed)
        self.programs = self._generate_programs()

    def _generate_programs(self):
        """Generate 500 programs with programs #387-391 being GLITCHDEX MALL versions"""
        programs = []

        # Templates for realistic shareware names
        genres = {
            "solitaire": ["SOLITAIRE", "FREECELL", "SPIDER SOLITAIRE", "PYRAMID", "KLONDIKE"],
            "screensaver": ["SCREENSAVER", "STARFIELD", "FLYING TOASTER", "MATRIX", "FLYING LOGO"],
            "compression": ["PKZIP", "ARJSFX", "WINZIP", "LHARC", "STUFFIT"],
            "utility": ["UNINSTALL", "DISK DOCTOR", "DEFRAG", "CACHE CLEANER", "OPTIMIZER"],
            "editor": ["NOTEPAD PRO", "TEXTVIEW", "EDITOR PLUS", "WORDPAD", "RICHTEXT"],
            "graphics": ["PAINT", "IMAGEVUE", "VIEWER PRO", "THUMBNAILER", "CONVERTER"],
            "sound": ["WINAMP", "MEDIA PLAYER", "WAVEFORM", "CONVERTER", "MIXER"],
            "demo": ["DEMO", "TECH DEMO", "3D DEMO", "SCENE DEMO", "INTRO"],
            "game": ["TETRIS", "CHESS", "CHECKERS", "POKER", "BINGO"],
            "productivity": ["CALCULATOR", "ORGANIZER", "TODO", "TIMER", "CLOCK"],
            "network": ["PING", "DIALER", "MODEM", "TERMINAL", "TRANSFER"],
            "system": ["MONITOR", "BENCHMARK", "INFO", "ANALYZER", "CHECKER"],
        }

        versions = ["1.0", "1.1", "2.0", "3.2", "4.5", "5.0", "LITE", "PRO", "DELUXE", ""]

        adjectives = ["ULTRA", "MEGA", "SUPER", "EXTREME", "POWER", "TURBO", "CHAOS", "ULTIMATE"]

        programs_list = []

        # Generate 500 programs
        for i in range(1, 501):
            if i == 387:
                # V1: Original retro game
                programs_list.append({
                    "number": i,
                    "name": "GLITCHDEX MALL - Original",
                    "genre": "game",
                    "version": "1.0",
                    "executable": "v1",
                    "is_real": True,
                    "description": "Original Wolf3D-style retro mall crawler"
                })
            elif i == 388:
                # V2: Immersive sim
                programs_list.append({
                    "number": i,
                    "name": "GLITCHDEX MALL - Immersive Sim",
                    "genre": "game",
                    "version": "2.0",
                    "executable": "v2",
                    "is_real": True,
                    "description": "Advanced AI architecture with factions & stealth"
                })
            elif i == 389:
                # V3: Eastland Mall - Full graphical with AI
                programs_list.append({
                    "number": i,
                    "name": "EASTLAND MALL - Graphical Engine",
                    "genre": "game",
                    "version": "3.0",
                    "executable": "v3",
                    "is_real": True,
                    "description": "Pygame raycaster with all V2 systems"
                })
            elif i == 390:
                # V4: Renderist Mall OS - Cloud-driven world
                programs_list.append({
                    "number": i,
                    "name": "RENDERIST MALL OS - Cloud World",
                    "genre": "game",
                    "version": "4.0",
                    "executable": "v4",
                    "is_real": True,
                    "description": "Cloud-driven semantic space architecture"
                })
            elif i == 391:
                # V5: Eastland CRD Reconstruction
                programs_list.append({
                    "number": i,
                    "name": "EASTLAND MALL - CRD Reconstruction",
                    "genre": "documentation",
                    "version": "5.0",
                    "executable": "v5",
                    "is_real": True,
                    "description": "Classification Reference Document methodology"
                })
            elif i == 392:
                # V6: Next Generation (placeholder)
                programs_list.append({
                    "number": i,
                    "name": "GLITCHDEX MALL - Next Generation",
                    "genre": "game",
                    "version": "6.0",
                    "executable": "v6",
                    "is_real": True,
                    "description": "Future development placeholder"
                })
            else:
                # Generate fake program
                genre = random.choice(list(genres.keys()))
                base_name = random.choice(genres[genre])

                # Sometimes add adjective
                if random.random() < 0.3:
                    base_name = random.choice(adjectives) + " " + base_name

                # Sometimes add version or variant
                version_suffix = ""
                if random.random() < 0.6:
                    version_suffix = " " + random.choice(versions)

                full_name = base_name + version_suffix

                programs_list.append({
                    "number": i,
                    "name": full_name,
                    "genre": genre,
                    "version": random.choice(versions),
                    "executable": f"prog_{i}.exe",
                    "is_real": False,
                    "description": "Not installed"
                })

        return programs_list

    def get_program(self, number):
        """Get program by number"""
        for prog in self.programs:
            if prog["number"] == number:
                return prog
        return None

    def get_all_programs(self):
        """Get all programs"""
        return self.programs

    def get_programs_by_genre(self, genre):
        """Get programs by genre"""
        return [p for p in self.programs if p["genre"] == genre]

    def get_real_programs(self):
        """Get only real/installed programs"""
        return [p for p in self.programs if p["is_real"]]

    def get_random_programs(self, count=20):
        """Get random selection of programs"""
        return random.sample(self.programs, min(count, len(self.programs)))

    def export_catalog(self):
        """Export catalog text"""
        text = """
╔════════════════════════════════════════════════════════════════════════════╗
║                  GAMEZILLA MEGA COLLECTION VOL. 4                          ║
║               The Ultimate Shareware & Freeware Compilation                ║
║                                                                            ║
║  500 Programs • Your Entertainment Solution for 1998!                     ║
║  Complete with Games, Utilities, Demos, and MORE!                         ║
╚════════════════════════════════════════════════════════════════════════════╝

PROGRAM LISTING (Programs 1-500)

"""
        for prog in self.programs:
            marker = " [INSTALLED]" if prog["is_real"] else ""
            text += f"{prog['number']:3d}. {prog['name']:<50}{marker}\n"

        return text


if __name__ == "__main__":
    gen = SharewareGeneratorV2()

    # Show real programs
    print("Installed programs:\n")
    for prog in gen.get_real_programs():
        print(f"{prog['number']:3d}. {prog['name']}")
        print(f"     Description: {prog['description']}")
        print()

    # Export full catalog
    with open("PROGRAM_CATALOG_V2.txt", "w") as f:
        f.write(gen.export_catalog())
    print("\nCatalog exported to PROGRAM_CATALOG_V2.txt")
