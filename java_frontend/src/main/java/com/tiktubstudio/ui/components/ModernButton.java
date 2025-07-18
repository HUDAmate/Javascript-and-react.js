package com.tiktubstudio.ui.components;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.geom.RoundRectangle2D;

/**
 * Modern button component dengan Duolingo-inspired styling
 * Features: rounded corners, smooth hover effects, dan multiple style variants
 */
public class ModernButton extends JButton {
    
    public enum ButtonStyle {
        PRIMARY,    // Green background
        SECONDARY,  // Blue background  
        OUTLINE,    // Border only
        GHOST,      // No background
        DANGER      // Red background
    }
    
    private ButtonStyle buttonStyle;
    private String iconText;
    private boolean isHovered = false;
    private boolean isPressed = false;
    
    // Colors
    private static final Color PRIMARY_GREEN = new Color(88, 204, 2);
    private static final Color SECONDARY_BLUE = new Color(28, 176, 246);
    private static final Color DANGER_RED = new Color(255, 75, 75);
    private static final Color TEXT_WHITE = new Color(255, 255, 255);
    private static final Color TEXT_DARK = new Color(59, 72, 80);
    private static final Color BORDER_COLOR = new Color(229, 232, 235);
    
    public ModernButton(String text) {
        this(text, ButtonStyle.PRIMARY);
    }
    
    public ModernButton(String text, ButtonStyle style) {
        super(text);
        this.buttonStyle = style;
        initializeButton();
    }
    
    private void initializeButton() {
        setFocusPainted(false);
        setBorderPainted(false);
        setContentAreaFilled(false);
        setOpaque(false);
        setCursor(new Cursor(Cursor.HAND_CURSOR));
        
        // Set font
        setFont(new Font("Segoe UI", Font.BOLD, 14));
        
        // Set preferred size
        setPreferredSize(new Dimension(120, 40));
        
        // Add mouse listeners for hover effects
        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                isHovered = true;
                repaint();
            }
            
            @Override
            public void mouseExited(MouseEvent e) {
                isHovered = false;
                repaint();
            }
            
            @Override
            public void mousePressed(MouseEvent e) {
                isPressed = true;
                repaint();
            }
            
            @Override
            public void mouseReleased(MouseEvent e) {
                isPressed = false;
                repaint();
            }
        });
    }
    
    public void setIcon(String iconText) {
        this.iconText = iconText;
        repaint();
    }
    
    public void setButtonStyle(ButtonStyle style) {
        this.buttonStyle = style;
        repaint();
    }
    
    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2d = (Graphics2D) g.create();
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        int width = getWidth();
        int height = getHeight();
        int arc = 8;
        
        // Create rounded rectangle
        RoundRectangle2D roundRect = new RoundRectangle2D.Float(0, 0, width - 1, height - 1, arc, arc);
        
        // Apply button style
        Color backgroundColor = getBackgroundColor();
        Color textColor = getTextColor();
        
        // Apply hover and press effects
        if (isPressed) {
            backgroundColor = darkenColor(backgroundColor, 0.15f);
        } else if (isHovered) {
            backgroundColor = lightenColor(backgroundColor, 0.1f);
        }
        
        // Draw background
        if (buttonStyle != ButtonStyle.GHOST) {
            g2d.setColor(backgroundColor);
            g2d.fill(roundRect);
        }
        
        // Draw border for outline style
        if (buttonStyle == ButtonStyle.OUTLINE || buttonStyle == ButtonStyle.GHOST) {
            g2d.setColor(buttonStyle == ButtonStyle.OUTLINE ? getPrimaryColor() : BORDER_COLOR);
            g2d.setStroke(new BasicStroke(1.5f));
            g2d.draw(roundRect);
        }
        
        // Draw text and icon
        g2d.setColor(textColor);
        drawContent(g2d, width, height);
        
        g2d.dispose();
    }
    
    private void drawContent(Graphics2D g2d, int width, int height) {
        FontMetrics fm = g2d.getFontMetrics();
        String text = getText();
        
        int totalWidth = 0;
        int iconWidth = 0;
        int textWidth = 0;
        
        // Calculate dimensions
        if (iconText != null && !iconText.isEmpty()) {
            iconWidth = fm.stringWidth(iconText);
            totalWidth += iconWidth;
            if (text != null && !text.isEmpty()) {
                totalWidth += 8; // spacing
            }
        }
        
        if (text != null && !text.isEmpty()) {
            textWidth = fm.stringWidth(text);
            totalWidth += textWidth;
        }
        
        // Calculate starting position (centered)
        int startX = (width - totalWidth) / 2;
        int centerY = (height - fm.getHeight()) / 2 + fm.getAscent();
        
        // Draw icon
        if (iconText != null && !iconText.isEmpty()) {
            g2d.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 16));
            FontMetrics iconFm = g2d.getFontMetrics();
            int iconY = (height - iconFm.getHeight()) / 2 + iconFm.getAscent();
            g2d.drawString(iconText, startX, iconY);
            startX += iconWidth + 8;
        }
        
        // Draw text
        if (text != null && !text.isEmpty()) {
            g2d.setFont(getFont());
            g2d.drawString(text, startX, centerY);
        }
    }
    
    private Color getBackgroundColor() {
        switch (buttonStyle) {
            case PRIMARY:
                return PRIMARY_GREEN;
            case SECONDARY:
                return SECONDARY_BLUE;
            case DANGER:
                return DANGER_RED;
            case OUTLINE:
            case GHOST:
            default:
                return Color.TRANSPARENT;
        }
    }
    
    private Color getTextColor() {
        switch (buttonStyle) {
            case PRIMARY:
            case SECONDARY:
            case DANGER:
                return TEXT_WHITE;
            case OUTLINE:
                return getPrimaryColor();
            case GHOST:
            default:
                return TEXT_DARK;
        }
    }
    
    private Color getPrimaryColor() {
        switch (buttonStyle) {
            case SECONDARY:
                return SECONDARY_BLUE;
            case DANGER:
                return DANGER_RED;
            case PRIMARY:
            case OUTLINE:
            case GHOST:
            default:
                return PRIMARY_GREEN;
        }
    }
    
    private Color lightenColor(Color color, float factor) {
        if (color == Color.TRANSPARENT) return color;
        
        float[] hsb = Color.RGBtoHSB(color.getRed(), color.getGreen(), color.getBlue(), null);
        hsb[2] = Math.min(1.0f, hsb[2] + factor);
        return Color.getHSBColor(hsb[0], hsb[1], hsb[2]);
    }
    
    private Color darkenColor(Color color, float factor) {
        if (color == Color.TRANSPARENT) return color;
        
        float[] hsb = Color.RGBtoHSB(color.getRed(), color.getGreen(), color.getBlue(), null);
        hsb[2] = Math.max(0.0f, hsb[2] - factor);
        return Color.getHSBColor(hsb[0], hsb[1], hsb[2]);
    }
    
    @Override
    public Dimension getPreferredSize() {
        Dimension size = super.getPreferredSize();
        
        // Minimum size
        size.width = Math.max(size.width, 100);
        size.height = Math.max(size.height, 40);
        
        // Add padding
        size.width += 32;
        size.height += 16;
        
        return size;
    }
}