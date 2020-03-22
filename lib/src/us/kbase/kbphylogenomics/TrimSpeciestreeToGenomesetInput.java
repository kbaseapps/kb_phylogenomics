
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
 * <p>Original spec-file type: trim_speciestree_to_genomeset_Input</p>
 * <pre>
 * trim_speciestree_to_genomeset()
 * **
 * ** reduce tree to match genomes found in genomeset
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_genomeSet_ref",
    "input_tree_ref",
    "output_tree_name",
    "desc",
    "show_skeleton_genome_sci_name",
    "enforce_genome_version_match",
    "reference_genome_disp",
    "skeleton_genome_disp",
    "user_genome_disp",
    "user2_genome_disp",
    "color_for_reference_genomes",
    "color_for_skeleton_genomes",
    "color_for_user_genomes",
    "color_for_user2_genomes",
    "tree_shape"
})
public class TrimSpeciestreeToGenomesetInput {

    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("input_genomeSet_ref")
    private java.lang.String inputGenomeSetRef;
    @JsonProperty("input_tree_ref")
    private java.lang.String inputTreeRef;
    @JsonProperty("output_tree_name")
    private java.lang.String outputTreeName;
    @JsonProperty("desc")
    private java.lang.String desc;
    @JsonProperty("show_skeleton_genome_sci_name")
    private Long showSkeletonGenomeSciName;
    @JsonProperty("enforce_genome_version_match")
    private Long enforceGenomeVersionMatch;
    @JsonProperty("reference_genome_disp")
    private Map<String, Map<String, String>> referenceGenomeDisp;
    @JsonProperty("skeleton_genome_disp")
    private Map<String, Map<String, String>> skeletonGenomeDisp;
    @JsonProperty("user_genome_disp")
    private Map<String, Map<String, String>> userGenomeDisp;
    @JsonProperty("user2_genome_disp")
    private Map<String, Map<String, String>> user2GenomeDisp;
    @JsonProperty("color_for_reference_genomes")
    private java.lang.String colorForReferenceGenomes;
    @JsonProperty("color_for_skeleton_genomes")
    private java.lang.String colorForSkeletonGenomes;
    @JsonProperty("color_for_user_genomes")
    private java.lang.String colorForUserGenomes;
    @JsonProperty("color_for_user2_genomes")
    private java.lang.String colorForUser2Genomes;
    @JsonProperty("tree_shape")
    private java.lang.String treeShape;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public TrimSpeciestreeToGenomesetInput withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_genomeSet_ref")
    public java.lang.String getInputGenomeSetRef() {
        return inputGenomeSetRef;
    }

    @JsonProperty("input_genomeSet_ref")
    public void setInputGenomeSetRef(java.lang.String inputGenomeSetRef) {
        this.inputGenomeSetRef = inputGenomeSetRef;
    }

    public TrimSpeciestreeToGenomesetInput withInputGenomeSetRef(java.lang.String inputGenomeSetRef) {
        this.inputGenomeSetRef = inputGenomeSetRef;
        return this;
    }

    @JsonProperty("input_tree_ref")
    public java.lang.String getInputTreeRef() {
        return inputTreeRef;
    }

    @JsonProperty("input_tree_ref")
    public void setInputTreeRef(java.lang.String inputTreeRef) {
        this.inputTreeRef = inputTreeRef;
    }

    public TrimSpeciestreeToGenomesetInput withInputTreeRef(java.lang.String inputTreeRef) {
        this.inputTreeRef = inputTreeRef;
        return this;
    }

    @JsonProperty("output_tree_name")
    public java.lang.String getOutputTreeName() {
        return outputTreeName;
    }

    @JsonProperty("output_tree_name")
    public void setOutputTreeName(java.lang.String outputTreeName) {
        this.outputTreeName = outputTreeName;
    }

    public TrimSpeciestreeToGenomesetInput withOutputTreeName(java.lang.String outputTreeName) {
        this.outputTreeName = outputTreeName;
        return this;
    }

    @JsonProperty("desc")
    public java.lang.String getDesc() {
        return desc;
    }

    @JsonProperty("desc")
    public void setDesc(java.lang.String desc) {
        this.desc = desc;
    }

    public TrimSpeciestreeToGenomesetInput withDesc(java.lang.String desc) {
        this.desc = desc;
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

    public TrimSpeciestreeToGenomesetInput withShowSkeletonGenomeSciName(Long showSkeletonGenomeSciName) {
        this.showSkeletonGenomeSciName = showSkeletonGenomeSciName;
        return this;
    }

    @JsonProperty("enforce_genome_version_match")
    public Long getEnforceGenomeVersionMatch() {
        return enforceGenomeVersionMatch;
    }

    @JsonProperty("enforce_genome_version_match")
    public void setEnforceGenomeVersionMatch(Long enforceGenomeVersionMatch) {
        this.enforceGenomeVersionMatch = enforceGenomeVersionMatch;
    }

    public TrimSpeciestreeToGenomesetInput withEnforceGenomeVersionMatch(Long enforceGenomeVersionMatch) {
        this.enforceGenomeVersionMatch = enforceGenomeVersionMatch;
        return this;
    }

    @JsonProperty("reference_genome_disp")
    public Map<String, Map<String, String>> getReferenceGenomeDisp() {
        return referenceGenomeDisp;
    }

    @JsonProperty("reference_genome_disp")
    public void setReferenceGenomeDisp(Map<String, Map<String, String>> referenceGenomeDisp) {
        this.referenceGenomeDisp = referenceGenomeDisp;
    }

    public TrimSpeciestreeToGenomesetInput withReferenceGenomeDisp(Map<String, Map<String, String>> referenceGenomeDisp) {
        this.referenceGenomeDisp = referenceGenomeDisp;
        return this;
    }

    @JsonProperty("skeleton_genome_disp")
    public Map<String, Map<String, String>> getSkeletonGenomeDisp() {
        return skeletonGenomeDisp;
    }

    @JsonProperty("skeleton_genome_disp")
    public void setSkeletonGenomeDisp(Map<String, Map<String, String>> skeletonGenomeDisp) {
        this.skeletonGenomeDisp = skeletonGenomeDisp;
    }

    public TrimSpeciestreeToGenomesetInput withSkeletonGenomeDisp(Map<String, Map<String, String>> skeletonGenomeDisp) {
        this.skeletonGenomeDisp = skeletonGenomeDisp;
        return this;
    }

    @JsonProperty("user_genome_disp")
    public Map<String, Map<String, String>> getUserGenomeDisp() {
        return userGenomeDisp;
    }

    @JsonProperty("user_genome_disp")
    public void setUserGenomeDisp(Map<String, Map<String, String>> userGenomeDisp) {
        this.userGenomeDisp = userGenomeDisp;
    }

    public TrimSpeciestreeToGenomesetInput withUserGenomeDisp(Map<String, Map<String, String>> userGenomeDisp) {
        this.userGenomeDisp = userGenomeDisp;
        return this;
    }

    @JsonProperty("user2_genome_disp")
    public Map<String, Map<String, String>> getUser2GenomeDisp() {
        return user2GenomeDisp;
    }

    @JsonProperty("user2_genome_disp")
    public void setUser2GenomeDisp(Map<String, Map<String, String>> user2GenomeDisp) {
        this.user2GenomeDisp = user2GenomeDisp;
    }

    public TrimSpeciestreeToGenomesetInput withUser2GenomeDisp(Map<String, Map<String, String>> user2GenomeDisp) {
        this.user2GenomeDisp = user2GenomeDisp;
        return this;
    }

    @JsonProperty("color_for_reference_genomes")
    public java.lang.String getColorForReferenceGenomes() {
        return colorForReferenceGenomes;
    }

    @JsonProperty("color_for_reference_genomes")
    public void setColorForReferenceGenomes(java.lang.String colorForReferenceGenomes) {
        this.colorForReferenceGenomes = colorForReferenceGenomes;
    }

    public TrimSpeciestreeToGenomesetInput withColorForReferenceGenomes(java.lang.String colorForReferenceGenomes) {
        this.colorForReferenceGenomes = colorForReferenceGenomes;
        return this;
    }

    @JsonProperty("color_for_skeleton_genomes")
    public java.lang.String getColorForSkeletonGenomes() {
        return colorForSkeletonGenomes;
    }

    @JsonProperty("color_for_skeleton_genomes")
    public void setColorForSkeletonGenomes(java.lang.String colorForSkeletonGenomes) {
        this.colorForSkeletonGenomes = colorForSkeletonGenomes;
    }

    public TrimSpeciestreeToGenomesetInput withColorForSkeletonGenomes(java.lang.String colorForSkeletonGenomes) {
        this.colorForSkeletonGenomes = colorForSkeletonGenomes;
        return this;
    }

    @JsonProperty("color_for_user_genomes")
    public java.lang.String getColorForUserGenomes() {
        return colorForUserGenomes;
    }

    @JsonProperty("color_for_user_genomes")
    public void setColorForUserGenomes(java.lang.String colorForUserGenomes) {
        this.colorForUserGenomes = colorForUserGenomes;
    }

    public TrimSpeciestreeToGenomesetInput withColorForUserGenomes(java.lang.String colorForUserGenomes) {
        this.colorForUserGenomes = colorForUserGenomes;
        return this;
    }

    @JsonProperty("color_for_user2_genomes")
    public java.lang.String getColorForUser2Genomes() {
        return colorForUser2Genomes;
    }

    @JsonProperty("color_for_user2_genomes")
    public void setColorForUser2Genomes(java.lang.String colorForUser2Genomes) {
        this.colorForUser2Genomes = colorForUser2Genomes;
    }

    public TrimSpeciestreeToGenomesetInput withColorForUser2Genomes(java.lang.String colorForUser2Genomes) {
        this.colorForUser2Genomes = colorForUser2Genomes;
        return this;
    }

    @JsonProperty("tree_shape")
    public java.lang.String getTreeShape() {
        return treeShape;
    }

    @JsonProperty("tree_shape")
    public void setTreeShape(java.lang.String treeShape) {
        this.treeShape = treeShape;
    }

    public TrimSpeciestreeToGenomesetInput withTreeShape(java.lang.String treeShape) {
        this.treeShape = treeShape;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((((((((((((((((((((((("TrimSpeciestreeToGenomesetInput"+" [workspaceName=")+ workspaceName)+", inputGenomeSetRef=")+ inputGenomeSetRef)+", inputTreeRef=")+ inputTreeRef)+", outputTreeName=")+ outputTreeName)+", desc=")+ desc)+", showSkeletonGenomeSciName=")+ showSkeletonGenomeSciName)+", enforceGenomeVersionMatch=")+ enforceGenomeVersionMatch)+", referenceGenomeDisp=")+ referenceGenomeDisp)+", skeletonGenomeDisp=")+ skeletonGenomeDisp)+", userGenomeDisp=")+ userGenomeDisp)+", user2GenomeDisp=")+ user2GenomeDisp)+", colorForReferenceGenomes=")+ colorForReferenceGenomes)+", colorForSkeletonGenomes=")+ colorForSkeletonGenomes)+", colorForUserGenomes=")+ colorForUserGenomes)+", colorForUser2Genomes=")+ colorForUser2Genomes)+", treeShape=")+ treeShape)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
