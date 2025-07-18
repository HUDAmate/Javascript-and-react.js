package com.tiktubstudio.ui.components;

import javax.swing.*;
import java.awt.*;
import java.awt.geom.RoundRectangle2D;

/**
 * Panel dengan rounded corners untuk modern card design
 */
public class RoundedPanel extends JPanel {
    private int cornerRadius;
    private Color backgroundColor;
    private boolean hasShadow;
    
    public RoundedPanel(int cornerRadius) {
        this(cornerRadius, Color.WHITE, false);
    }
    
    public RoundedPanel(int cornerRadius, Color backgroundColor, boolean hasShadow) {
        this.cornerRadius = cornerRadius;
        this.backgroundColor = backgroundColor;
        this.hasShadow = hasShadow;
        
        setOpaque(false);
    }
    
    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2d = (Graphics2D) g.create();
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        int width = getWidth();
        int height = getHeight();
        
        // Draw shadow if enabled
        if (hasShadow) {
            drawShadow(g2d, width, height);
        }
        
        // Draw background
        if (backgroundColor != null) {
            g2d.setColor(backgroundColor);
            RoundRectangle2D roundRect = new RoundRectangle2D.Float(0, 0, width, height, cornerRadius, cornerRadius);
            g2d.fill(roundRect);
        }
        
        g2d.dispose();
        super.paintComponent(g);
    }
    
    private void drawShadow(Graphics2D g2d, int width, int height) {
        // Simple shadow effect
        int shadowOffset = 2;
        Color shadowColor = new Color(0, 0, 0, 20);
        
        g2d.setColor(shadowColor);
        RoundRectangle2D shadowRect = new RoundRectangle2D.Float(
            shadowOffset, shadowOffset, 
            width - shadowOffset, height - shadowOffset, 
            cornerRadius, cornerRadius
        );
        g2d.fill(shadowRect);
    }
    
    @Override
    public void setBackground(Color bg) {
        this.backgroundColor = bg;
        repaint();
    }
    
    @Override
    public Color getBackground() {
        return backgroundColor;
    }
    
    public void setShadowEnabled(boolean enabled) {
        this.hasShadow = enabled;
        repaint();
    }
    
    public void setCornerRadius(int radius) {
        this.cornerRadius = radius;
        repaint();
    }
}