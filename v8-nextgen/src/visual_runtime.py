#!/usr/bin/env python3
"""
NINJA SABOTEUR: VISUAL RUNTIME
Entry point for the CRAY-style simulation.
"""

import sys
import pygame
import math
from pathlib import Path

# Ensure imports work from src root
sys.path.append(str(Path(__file__).parent))

from game_loop import NinjaGameMode

TILE_SIZE = 24
SCREEN_W, SCREEN_H = 1280, 800
COLORS = {
    "BG": (10, 15, 20), "GRID": (30, 40, 50), "WALL": (60, 70, 80),
    "PLAYER": (0, 255, 100), "JANITOR": (255, 50, 50),
    "TRACE_HIGH": (0, 255, 255), "TRACE_LOW": (255, 100, 0),
    "CLOUD": (200, 200, 255), "TEXT": (0, 255, 0)
}

class VisualRuntime:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("FW_NINJA_SABOTEUR // CRAY_RUNTIME")
        self.font = pygame.font.SysFont("Consolas", 14)
        self.clock = pygame.time.Clock()
        self.sim = None
        self.cam_x, self.cam_y = 0, 0
        self.selected = "SMOKE_PELLET"
        self.keys = {
            pygame.K_1: "SMOKE_PELLET", pygame.K_2: "IMPROVISED_COVER",
            pygame.K_3: "MESS_LURE_B", pygame.K_4: "COIN_TOSS"
        }
        self.load_level("game_state_foodcourt_v1.json")

    def load_level(self, fname):
        try:
            self.sim = NinjaGameMode(fname)
        except Exception as e:
            print(f"[ERR] Load failed: {e}")

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
            cmd = None
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT: return
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE: return
                    if e.key == pygame.K_UP: cmd = {'action':'MOVE','dir':(0,-1)}
                    if e.key == pygame.K_DOWN: cmd = {'action':'MOVE','dir':(0,1)}
                    if e.key == pygame.K_LEFT: cmd = {'action':'MOVE','dir':(-1,0)}
                    if e.key == pygame.K_RIGHT: cmd = {'action':'MOVE','dir':(1,0)}
                    if e.key == pygame.K_SPACE: cmd = {'action':'CONSTRUCT','type':self.selected}
                    if e.key in self.keys: self.selected = self.keys[e.key]
                    if e.key == pygame.K_F1: self.load_level("game_state_foodcourt_v1.json")
                    if e.key == pygame.K_F2: self.load_level("game_state_servicehall_v1.json")

            state = self.sim.tick(dt, cmd)
            self.draw(state)
            pygame.display.flip()

    def draw(self, state):
        self.screen.fill(COLORS["BG"])
        px, py = self.sim.player_pos
        self.cam_x += ((px*TILE_SIZE - SCREEN_W//2) - self.cam_x) * 0.1
        self.cam_y += ((py*TILE_SIZE - SCREEN_H//2) - self.cam_y) * 0.1
        ox, oy = -int(self.cam_x), -int(self.cam_y)

        # Grid & Heatmap
        for y, row in enumerate(self.sim.grid.tiles):
            for x, tile in enumerate(row):
                r = (x*TILE_SIZE+ox, y*TILE_SIZE+oy, TILE_SIZE, TILE_SIZE)
                if r[0]<-TILE_SIZE or r[0]>SCREEN_W or r[1]<-TILE_SIZE or r[1]>SCREEN_H: continue
                
                col = COLORS["WALL"] if tile.type == 1 else COLORS["GRID"]
                pygame.draw.rect(self.screen, col, r, 0 if tile.type==1 else 1)

                if (x,y) in self.sim.circuit_nodes:
                    s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    s.set_alpha(int(self.sim.circuit_nodes[(x,y)]["voltage"]*80))
                    s.fill((0,255,255))
                    self.screen.blit(s, r[:2])
                    # Construct Box
                    pygame.draw.rect(self.screen, (200,100,50), (r[0]+4,r[1]+4,16,16))

        # Traces
        nodes = list(self.sim.circuit_nodes.keys())
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i+1:]:
                dist = math.sqrt((n1[0]-n2[0])**2 + (n1[1]-n2[1])**2)
                if dist < 8.0:
                    start = (n1[0]*TILE_SIZE+12+ox, n1[1]*TILE_SIZE+12+oy)
                    end = (n2[0]*TILE_SIZE+12+ox, n2[1]*TILE_SIZE+12+oy)
                    snr = self.sim.circuit_nodes[n1]["snr"]
                    col = COLORS["TRACE_HIGH"] if snr > 0.8 else COLORS["TRACE_LOW"]
                    pygame.draw.line(self.screen, col, start, end, max(1, int(3-dist/3)))

        # Entities
        pr = (px*TILE_SIZE+ox, py*TILE_SIZE+oy, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, COLORS["PLAYER"], pr)
        jr = (self.sim.janitor.pos_x*TILE_SIZE+ox, self.sim.janitor.pos_y*TILE_SIZE+oy, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, COLORS["JANITOR"], jr)

        # Cloud
        for p in self.sim.flock.particles:
            pygame.draw.circle(self.screen, COLORS["CLOUD"], (int(p.x*TILE_SIZE+ox), int(p.y*TILE_SIZE+oy)), 2)

        # HUD
        pygame.draw.rect(self.screen, (0,0,0), (0, SCREEN_H-100, SCREEN_W, 100))
        pygame.draw.line(self.screen, COLORS["TEXT"], (0, SCREEN_H-100), (SCREEN_W, SCREEN_H-100), 2)

        # FPS Debug Overlay (top-right)
        fps = self.clock.get_fps()
        fps_text = self.font.render(f"FPS: {fps:.1f}", True, COLORS["TEXT"])
        self.screen.blit(fps_text, (SCREEN_W - 100, 10))

        hud = [
            f"SYS: ONLINE | LEVEL: {state.get('level_id','N/A')}",
            f"FOCUS: {state['focus']:.1f}V | CLOUD: {state['cloud']:.1f}",
            f"OPCODE: {self.selected}"
        ]
        for i, l in enumerate(hud):
            self.screen.blit(self.font.render(l, True, COLORS["TEXT"]), (20, SCREEN_H-90+i*25))

if __name__ == "__main__":
    VisualRuntime().run()
