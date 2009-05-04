<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version="1.0">
  <xsl:import href="http://docbook.sourceforge.net/release/xsl/current/html/docbook.xsl"/>
  <xsl:param name="html.stylesheet" select="'manual.css'"/>
  <xsl:param name="toc.section.depth">3</xsl:param>
  <xsl:param name="generate.section.toc.level" select="0"></xsl:param>
  <xsl:param name="section.autolabel" select="1"></xsl:param>
  <xsl:param name="section.autolabel.max.depth" select="3"></xsl:param>
  <xsl:param name="section.label.includes.component.label" select="1"></xsl:param>
  <xsl:param name="table.cell.border.thickness">0</xsl:param>
</xsl:stylesheet>


