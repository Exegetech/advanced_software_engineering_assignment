public void displayGame(String mode) {
  if (mode.equals("small")) {
        setColorDepth(8);
        drawRect(screen, 1024, 768);
  } else if (mode.equals("medium")) {
        setColorDepth(16);
        drawRect(screen, 1600, 1200);
  }
}
