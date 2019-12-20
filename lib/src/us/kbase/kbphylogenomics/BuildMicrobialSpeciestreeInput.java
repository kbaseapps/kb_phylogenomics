
package us.kbase.kbphylogenomics;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: build_microbial_speciestree_Input</p>
 * <pre>
 * build_microbial_speciestree()
 * **
 * ** run Insert Set of Genomes into Species Tree with extra features
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_genome_refs",
    "output_tree_name",
    "desc",
    "genome_disp_name_config",
    "show_skeleton_genome_sci_name",
    "skeleton_set",
    "num_proximal_sisters",
    "proximal_sisters_ANI_spacing",
    "color_for_reference_genomes",
    "color_for_skeleton_genomes",
    "color_for_user_genomes",
    "color_for_user2_genomes",
    "tree_shape"
})
public class BuildMicrobialSpeciestreeInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_genome_refs")
    private String inputGenomeRefs;
    @JsonProperty("output_tree_name")
    private String outputTreeName;
    @JsonProperty("desc")
    private String desc;
    @JsonProperty("genome_disp_name_config")
    private String genomeDispNameConfig;
    @JsonProperty("show_skeleton_genome_sci_name")
    private Long showSkeletonGenomeSciName;
    @JsonProperty("skeleton_set")
    private String skeletonSet;
    @JsonProperty("num_proximal_sisters")
    private Long numProximalSisters;
    @JsonProperty("proximal_sisters_ANI_spacing")
    private Double proximalSistersANISpacing;
    @JsonProperty("color_for_reference_genomes")
    private String colorForReferenceGenomes;
    @JsonProperty("color_for_skeleton_genomes")
    private String colorForSkeletonGenomes;
    @JsonProperty("color_for_user_genomes")
    private String colorForUserGenomes;
    @JsonProperty("color_for_user2_genomes")
    private String colorForUser2Genomes;
    @JsonProperty("tree_shape")
    private String treeShape;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public BuildMicrobialSpeciestreeInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_genome_refs")
    public String getInputGenomeRefs() {
        return inputGenomeRefs;
    }

    @JsonProperty("input_genome_refs")
    public void setInputGenomeRefs(String inputGenomeRefs) {
        this.inputGenomeRefs = inputGenomeRefs;
    }

    public BuildMicrobialSpeciestreeInput withInputGenomeRefs(String inputGenomeRefs) {
        this.inputGenomeRefs = inputGenomeRefs;
        return this;
    }

    @JsonProperty("output_tree_name")
    public String getOutputTreeName() {
        return outputTreeName;
    }

    @JsonProperty("output_tree_name")
    public void setOutputTreeName(String outputTreeName) {
        this.outputTreeName = outputTreeName;
    }

    public BuildMicrobialSpeciestreeInput withOutputTreeName(String outputTreeName) {
        this.outputTreeName = outputTreeName;
        return this;
    }

    @JsonProperty("desc")
    public String getDesc() {
        return desc;
    }

    @JsonProperty("desc")
    public void setDesc(String desc) {
        this.desc = desc;
    }

    public BuildMicrobialSpeciestreeInput withDesc(String desc) {
        this.desc = desc;
        return this;
    }

    @JsonProperty("genome_disp_name_config")
    public String getGenomeDispNameConfig() {
        return genomeDispNameConfig;
    }

    @JsonProperty("genome_disp_name_config")
    public void setGenomeDispNameConfig(String genomeDispNameConfig) {
        this.genomeDispNameConfig = genomeDispNameConfig;
    }

    public BuildMicrobialSpeciestreeInput withGenomeDispNameConfig(String genomeDispNameConfig) {
        this.genomeDispNameConfig = genomeDispNameConfig;
        return this;
    }

    @JsonProperty("show_skeleton_genome_sci_name")
    public Long getShowSkeletonGenomeSciName() {
        return showSkeletonGenomeSciName;
    }

    @JsonProperty("show_skeleton_genome_sci_name")
    public void setShowSkeletonGenomeSciName(Long showSkeletonGenomeSciName) {
        this.showSkeletonGenomeSciName = showSkeletonGenomeSciName;
    }

    public BuildMicrobialSpeciestreeInput withShowSkeletonGenomeSciName(Long showSkeletonGenomeSciName) {
        this.showSkeletonGenomeSciName = showSkeletonGenomeSciName;
        return this;
    }

    @JsonProperty("skeleton_set")
    public String getSkeletonSet() {
        return skeletonSet;
    }

    @JsonProperty("skeleton_set")
    public void setSkeletonSet(String skeletonSet) {
        this.skeletonSet = skeletonSet;
    }

    public BuildMicrobialSpeciestreeInput withSkeletonSet(String skeletonSet) {
        this.skeletonSet = skeletonSet;
        return this;
    }

    @JsonProperty("num_proximal_sisters")
    public Long getNumProximalSisters() {
        return numProximalSisters;
    }

    @JsonProperty("num_proximal_sisters")
    public void setNumProximalSisters(Long numProximalSisters) {
        this.numProximalSisters = numProximalSisters;
    }

    public BuildMicrobialSpeciestreeInput withNumProximalSisters(Long numProximalSisters) {
        this.numProximalSisters = numProximalSisters;
        return this;
    }

    @JsonProperty("proximal_sisters_ANI_spacing")
    public Double getProximalSistersANISpacing() {
        return proximalSistersANISpacing;
    }

    @JsonProperty("proximal_sisters_ANI_spacing")
    public void setProximalSistersANISpacing(Double proximalSistersANISpacing) {
        this.proximalSistersANISpacing = proximalSistersANISpacing;
    }

    public BuildMicrobialSpeciestreeInput withProximalSistersANISpacing(Double proximalSistersANISpacing) {
        this.proximalSistersANISpacing = proximalSistersANISpacing;
        return this;
    }

    @JsonProperty("color_for_reference_genomes")
    public String getColorForReferenceGenomes() {
        return colorForReferenceGenomes;
    }

    @JsonProperty("color_for_reference_genomes")
    public void setColorForReferenceGenomes(String colorForReferenceGenomes) {
        this.colorForReferenceGenomes = colorForReferenceGenomes;
    }

    public BuildMicrobialSpeciestreeInput withColorForReferenceGenomes(String colorForReferenceGenomes) {
        this.colorForReferenceGenomes = colorForReferenceGenomes;
        return this;
    }

    @JsonProperty("color_for_skeleton_genomes")
    public String getColorForSkeletonGenomes() {
        return colorForSkeletonGenomes;
    }

    @JsonProperty("color_for_skeleton_genomes")
    public void setColorForSkeletonGenomes(String colorForSkeletonGenomes) {
        this.colorForSkeletonGenomes = colorForSkeletonGenomes;
    }

    public BuildMicrobialSpeciestreeInput withColorForSkeletonGenomes(String colorForSkeletonGenomes) {
        this.colorForSkeletonGenomes = colorForSkeletonGenomes;
        return this;
    }

    @JsonProperty("color_for_user_genomes")
    public String getColorForUserGenomes() {
        return colorForUserGenomes;
    }

    @JsonProperty("color_for_user_genomes")
    public void setColorForUserGenomes(String colorForUserGenomes) {
        this.colorForUserGenomes = colorForUserGenomes;
    }

    public BuildMicrobialSpeciestreeInput withColorForUserGenomes(String colorForUserGenomes) {
        this.colorForUserGenomes = colorForUserGenomes;
        return this;
    }

    @JsonProperty("color_for_user2_genomes")
    public String getColorForUser2Genomes() {
        return colorForUser2Genomes;
    }

    @JsonProperty("color_for_user2_genomes")
    public void setColorForUser2Genomes(String colorForUser2Genomes) {
        this.colorForUser2Genomes = colorForUser2Genomes;
    }

    public BuildMicrobialSpeciestreeInput withColorForUser2Genomes(String colorForUser2Genomes) {
        this.colorForUser2Genomes = colorForUser2Genomes;
        return this;
    }

    @JsonProperty("tree_shape")
    public String getTreeShape() {
        return treeShape;
    }

    @JsonProperty("tree_shape")
    public void setTreeShape(String treeShape) {
        this.treeShape = treeShape;
    }

    public BuildMicrobialSpeciestreeInput withTreeShape(String treeShape) {
        this.treeShape = treeShape;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((((((((((((("BuildMicrobialSpeciestreeInput"+" [workspaceName=")+ workspaceName)+", inputGenomeRefs=")+ inputGenomeRefs)+", outputTreeName=")+ outputTreeName)+", desc=")+ desc)+", genomeDispNameConfig=")+ genomeDispNameConfig)+", showSkeletonGenomeSciName=")+ showSkeletonGenomeSciName)+", skeletonSet=")+ skeletonSet)+", numProximalSisters=")+ numProximalSisters)+", proximalSistersANISpacing=")+ proximalSistersANISpacing)+", colorForReferenceGenomes=")+ colorForReferenceGenomes)+", colorForSkeletonGenomes=")+ colorForSkeletonGenomes)+", colorForUserGenomes=")+ colorForUserGenomes)+", colorForUser2Genomes=")+ colorForUser2Genomes)+", treeShape=")+ treeShape)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
